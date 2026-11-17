# LP III - Group C
## Blockchain Technology
SPPU | Fourth Year Computer Engineering | 2019 Course | 410246

All four assignments from the supplied LP III.pdf. C1 and C2 are practical wallet exercises, so they include procedures and observations rather than unnecessary application code. C3 and C4 contain complete Solidity contracts.

Use a learning wallet and Sepolia test ETH. These instructions do not create a wallet, send funds or deploy anything on your behalf. Record actual transaction receipts after performing the exercises. Solidity contracts are teaching examples, not audited banking software.

## Common setup
- MetaMask: https://metamask.io/
- MetaMask network help: https://support.metamask.io/configure/networks
- Remix IDE: https://remix.ethereum.org/
- Sepolia explorer: https://sepolia.etherscan.io/
- Use a Solidity 0.8.x compiler satisfying pragma ^0.8.20, with the same compiler settings throughout comparisons.
- Practise contract calls in Remix VM first. Then select Remix's browser-wallet environment (often labelled Injected Provider - MetaMask) and verify MetaMask is on Sepolia before deploying. Menu wording can vary by version.

Never put the Secret Recovery Phrase or private key in code, reports, screenshots or chat. A public address may be recorded for transactions; the recovery phrase must stay private.

## C1. Install MetaMask and study Ether spent per transaction
**Aim:** Install a wallet and observe how network fees are calculated.

### Procedure
1. Open the official MetaMask website and choose the extension for a supported browser. Install through the linked official extension-store listing.
2. Open MetaMask and complete the wallet onboarding. If using recovery-phrase setup, back up the phrase privately and confirm it. The local password unlocks the extension; it is not a replacement for a recovery backup.
3. Open the network selector, enable test networks where needed and choose Sepolia.
4. Obtain a small amount of Sepolia test ETH from a faucet linked by a reputable network or wallet documentation source. Faucet eligibility varies; do not purchase mainnet ETH merely to complete this exercise.
5. Create or use a second test account as the receiving address.
6. Send a small test amount, such as 0.001 Sepolia ETH. Verify the recipient and network, review the estimated fee, and confirm.
7. After inclusion, open the transaction in the explorer. Record its status, transaction hash, value, gas used and effective gas price.
8. Calculate the actual fee and compare it with the pre-submission estimate. Estimates and actual fees can differ.

### Fee calculation
**Actual transaction fee in ETH = gasUsed × effectiveGasPrice in wei / 10^18.**

1 ETH = 10^18 wei. 1 gwei = 10^9 wei.
For an EIP-1559 transaction, effective price is limited by the max fee and includes the base fee plus the effective priority tip. The maximum fee is a cap, not necessarily what is charged.

**Illustrative example, not a measured transaction:** gas used = 21,000 and effective gas price = 2 gwei. Fee = 21,000 × 2 × 10^-9 = 0.000042 ETH. Sending 0.001 ETH therefore costs the sender 0.001042 ETH when this is the only balance-changing action.

A basic empty-data transfer between ordinary accounts commonly uses 21,000 gas. Contract execution can use more. gasLimit is the allowed upper bound, not the same as gasUsed. Failed included transactions can still consume gas.

### Optional calculation code - c1_fee.py
```python
from decimal import Decimal

gas_used = int(input("Gas used from receipt: "))
price_gwei = Decimal(input("Effective gas price in gwei: "))
value_eth = Decimal(input("Value transferred in ETH: "))
if gas_used < 0 or price_gwei < 0 or value_eth < 0:
    raise ValueError("Values cannot be negative")
fee_eth = Decimal(gas_used) * price_gwei / Decimal(10 ** 9)
print("Actual fee (ETH):", fee_eth)
print("Value + fee (ETH):", value_eth + fee_eth)
```
Run using `python3 c1_fee.py`. The calculation assumes a successful ordinary transfer; for a reverted transfer, the value is not transferred even though a fee may be paid.

### Observation table to complete
| Field | Value from your transaction |
|---|---|
| Network | Sepolia |
| Transaction hash | Record actual hash |
| Status | Record actual status |
| Value (ETH) | Record actual value |
| Gas limit | Record submitted limit |
| Gas used | Record receipt value |
| Effective gas price (gwei) | Record actual price |
| Calculated fee (ETH) | Compute from receipt |

**Tell the examiner:** "Ether is the asset; gas measures computational work. The network fee equals gas actually used multiplied by the effective gas price. The transferred amount and the fee are separate."

**Viva:** Does a read-only balance lookup require a paid transaction? Not when performed as an off-chain call. Does higher gas limit always mean higher fee? No; fees normally depend on gas actually used.

## C2. Create your own wallet for crypto transactions
**Aim:** Create a test wallet, identify its public address and demonstrate sending and receiving.

### Procedure
1. In MetaMask, create a new wallet through the offered onboarding flow, or use the dedicated learning wallet from C1.
2. Record the public address in the practical record. Do not record the recovery phrase.
3. Add a second account through MetaMask's account-management menu. Accounts derived from the same wallet backup are separate addresses, not independent recovery backups.
4. Select Sepolia for both accounts. Obtain test ETH in Account 1.
5. Copy Account 2's public address and check it carefully.
6. From Account 1, send a small test amount to Account 2. Keep enough test ETH for the network fee.
7. Confirm the transaction and inspect its receipt. Switch to Account 2 to observe the received amount.
8. Optionally send a smaller test amount back, leaving enough in Account 2 for its own fee.

**Expected observation:** Account 1 decreases by sent value plus fee; Account 2 increases by sent value. A later return transfer costs Account 2 another fee. Compare balances only after confirmation and with no other intervening transactions.

### Concepts to explain
- **Public address:** Identifier others use to send assets to the account.
- **Private key:** Secret used to authorize transactions by signing.
- **Recovery phrase:** Backup material that can restore derived accounts. Losing or revealing it can compromise access.
- **Nonce:** Per-account sequence number used to order transactions and prevent simple replay on that chain.
- **Wallet versus blockchain:** The wallet manages keys and signs requests; balances and confirmed transactions are recorded on the network.
- **Network:** The same address can exist on different networks, with different balances. Sepolia ETH is separate from mainnet ETH.

**Tell the examiner:** "I created a wallet, selected the test network and transferred test ETH between two public addresses. The wallet signed the transaction, and the blockchain recorded it after inclusion."

**Viva:** Is deleting the extension the same as deleting on-chain funds? No; access depends on preserving the correct backup. Should the recipient share a private key? Never; only the public receiving address is needed.

## C3. Bank account contract: deposit, withdraw and balance
**Aim:** Implement an Ether bank with a separate credited balance for each customer address.

**Design:** The sender deposits msg.value into their own ledger entry. They can withdraw only from that entry. Checks happen first, state is updated next, then the Ether transfer occurs. A reentrancy guard prevents nested withdrawals. An ordinary direct transfer invokes receive(), which credits the sender too.

### Code - Bank.sol
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Bank {
    mapping(address => uint256) private balances;
    bool private locked;

    event Deposited(address indexed customer, uint256 amount);
    event Withdrawn(address indexed customer, uint256 amount);

    modifier nonReentrant() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }

    function deposit() public payable {
        require(msg.value > 0, "Send positive ETH");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be positive");
        require(balances[msg.sender] >= amount,
                "Insufficient balance");

        balances[msg.sender] -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
        emit Withdrawn(msg.sender, amount);
    }

    function getBalance() external view returns (uint256) {
        return balances[msg.sender];
    }

    function contractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    receive() external payable {
        deposit();
    }
}
```

### Explanation
- mapping associates each address with its deposited balance in wei.
- payable allows the deposit function to accept Ether.
- msg.sender is the caller and msg.value is the Ether attached to this call.
- require rejects invalid operations. If the transfer fails, the transaction reverts, including the earlier ledger deduction.
- nonReentrant wraps withdrawal with a lock; the underscore marks where the function body runs.
- getBalance returns the caller's credited balance; contractBalance reports all Ether held by the contract. They are different quantities.
- Events make deposits and withdrawals easy to inspect in receipts.
- There is no owner who can withdraw someone else's credited funds.

### Compile and deploy
1. Create Bank.sol in Remix, paste the complete code and compile with a compatible compiler.
2. Select Remix VM and deploy with Value set to 0.
3. Choose an account, set Value to 1 ether, and call deposit.
4. Reset Value to 0 for subsequent non-payable calls.
5. Call getBalance. Expected ledger: 1000000000000000000 wei.
6. Call withdraw with argument 400000000000000000 (0.4 ether).
7. Call getBalance again. Expected ledger: 600000000000000000 wei.
8. Switch to another account; its getBalance should be 0.
9. Try withdrawing more than the remaining ledger; the call must revert.
10. When ready, choose the browser-wallet environment, verify Sepolia and deploy again using test ETH. Repeat with much smaller amounts if faucet funds are limited.

**Important distinction:** The wallet's balance changes include gas costs; the customer's bank ledger contains deposited value minus withdrawn value only. In unusual cases, Ether can arrive outside the crediting path, so the contract's raw balance should not be assumed to equal the sum of all ledger entries in every possible scenario.

### Suggested tests
| Action | Expected behavior |
|---|---|
| Deposit positive value | Sender ledger increases |
| Deposit zero | Reverts |
| Withdraw within own balance | Sender ledger decreases |
| Withdraw more than balance | Reverts |
| Account B withdraws Account A's balance | Impossible through this interface |
| getBalance via read-only call | Returns wei without a new paid transaction |

**Tell the examiner:** "I keep customer balances in a mapping. Deposits credit the caller, and withdrawals check that caller's balance, reduce it before transferring Ether and use a lock to prevent reentrant withdrawals."

**Viva:** Is private storage secret? No; private controls Solidity-level access, not blockchain confidentiality. Why use call and check success? The transfer can fail, so failure must revert the ledger change.

## C4. Student data using structures, arrays and fallback
**Aim:** Store student records with a struct and array, demonstrate fallback behavior, deploy and inspect gas.

**Design:** The deployer is the owner and may add students. Records are public through a getter. Duplicate roll numbers are rejected. Only fictional student data should be placed on a public test chain.

The fallback is deliberately non-payable: it logs unknown non-empty calldata but rejects Ether. This demonstrates fallback without accepting funds that the contract cannot withdraw.

### Code - StudentRegistry.sol
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StudentRegistry {
    struct Student {
        uint256 rollNo;
        string name;
        string department;
    }

    Student[] private students;
    mapping(uint256 => bool) private usedRollNo;
    address public immutable owner;

    event StudentAdded(uint256 indexed rollNo, string name);
    event FallbackCalled(address indexed sender, bytes data);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    function addStudent(
        uint256 rollNo,
        string calldata name,
        string calldata department
    ) external onlyOwner {
        require(rollNo > 0, "Invalid roll number");
        require(!usedRollNo[rollNo], "Duplicate roll number");
        require(bytes(name).length > 0, "Name required");
        require(bytes(department).length > 0, "Department required");

        usedRollNo[rollNo] = true;
        students.push(Student(rollNo, name, department));
        emit StudentAdded(rollNo, name);
    }

    function getStudent(uint256 index)
        external
        view
        returns (uint256, string memory, string memory)
    {
        require(index < students.length, "Index out of range");
        Student storage student = students[index];
        return (
            student.rollNo, student.name, student.department
        );
    }

    function studentCount() external view returns (uint256) {
        return students.length;
    }

    fallback() external {
        emit FallbackCalled(msg.sender, msg.data);
    }
}
```

### Explanation
- struct groups roll number, name and department into one record.
- Student[] is a dynamic storage array that grows with push.
- usedRollNo checks duplicates without scanning the whole array.
- calldata holds read-only external function inputs; storage refers to persistent on-chain data; memory holds temporary return values.
- immutable owner is set once during construction.
- fallback runs when no function selector matches. With no receive function here, it can also handle empty calldata with zero value.
- Because fallback is non-payable, sending positive Ether to it reverts. A payable receive function would normally handle empty-calldata Ether transfers if present.

### Deploy and interact
1. Create StudentRegistry.sol in Remix and compile with the same compatible Solidity compiler used for Bank.sol.
2. Select Remix VM, Value 0, and deploy.
3. Call addStudent with rollNo = 1, name = "Student One", department = "Computer".
4. Call studentCount: expected 1.
5. Call getStudent(0): expected (1, "Student One", "Computer"). Array index 0 is distinct from roll number 1.
6. Try the same roll number again; expect a revert.
7. Switch account and attempt addStudent; expect "Only owner".
8. To demonstrate fallback, use Remix's low-level transaction controls on the deployed instance. Set Value = 0, calldata = 0x12345678 and send.
9. Inspect the receipt logs for FallbackCalled. If that selector happened to match an ABI function, choose another unmatched selector.
10. Send the same unmatched calldata with a nonzero Value in Remix VM; it should revert because fallback is not payable.
11. Switch to the browser-wallet environment with Sepolia selected and repeat deployment and successful calls using test ETH. Capture your actual gas and fee values.

### Gas observation table
| Operation | Gas used | Effective gas price | Actual fee |
|---|---|---|---|
| Contract deployment | Record receipt | Record receipt | Compute |
| addStudent | Record receipt | Record receipt | Compute |
| Fallback transaction | Record receipt | Record receipt | Compute |
| getStudent via read-only call | No paid transaction | Not applicable | No network fee |

Do not copy invented gas figures. Values depend on compiler settings, the operation, stored values and string lengths. Deployment stores code; addStudent writes persistent data; a read-only call can execute without sending a paid transaction. Sending a transaction to a view method is different and can still incur a fee.

**Tell the examiner:** "I represent each student with a structure and store the records in a dynamic array. The owner can add records, getters read them and the fallback logs calls with unrecognized function selectors. I compare gas consumption using transaction receipts."

**Viva:** Why is fallback different from receive? receive is for empty-calldata Ether reception; fallback covers unmatched calls and can cover empty calldata when receive is absent. Does fallback need payable? Only if it should accept Ether. Why not store real student details? Public-chain records are visible and difficult to remove.

## References and boundaries
Assignment scope: supplied SPPU LP III.pdf, Group C.

Official references:
- MetaMask networks: https://support.metamask.io/configure/networks
- Solidity receive/fallback explanation: https://www.soliditylang.org/blog/2020/03/23/fallback-receive-split/
- Solidity contracts: https://docs.solidity.org/en/latest/contracts.html
- Solidity withdrawal pattern: https://docs.solidity.org/en/latest/common-patterns.html

The examples explain implementation and testing steps. No wallet was created, no test or real funds were moved, and no contract deployment or gas measurement is claimed in this document.

