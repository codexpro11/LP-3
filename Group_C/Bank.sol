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
