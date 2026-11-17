# LP III - Runnable assignment files

15 assignments, organized into three group folders. Each group includes Explanations.md with the full explanations from the study documents.

## Group A - Algorithms (Java)

Open a terminal in Group_A and compile/run any file with `javac` and `java` (or run single-file source directly with `java`):

```bash
cd Group_A
javac A1_Fibonacci.java && java A1_Fibonacci
# or in Java 11+:
java A1_Fibonacci.java
```

| Assignment | File | Input |
|---|---|---|
| A1 Fibonacci | A1_Fibonacci.java | Number of terms |
| A2 Huffman encoding | A2_HuffmanEncoding.java | String or Character-Frequency Table |
| A2 Job sequencing | A2_JobSequencing.java | Number of jobs, Name/Deadline/Profit |
| A3 Fractional knapsack | A3_FractionalKnapsack.java | Number of items, Name/Weight/Value, Capacity |
| A4 0-1 knapsack | A4_ZeroOneKnapsack.java | Number of items, Weight/Value, Capacity |
| A5 Binomial coefficients | A5_Binomial.java | n and r |
| A6 Eight queens | A6_EightQueens.java | Fixed queen row/column, 1 to 8 |

## Group B - Machine learning

Use Python 3.10 or newer for a fresh setup. From Group_B:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 b1_uber.py
```

On Windows activate using `.venv\Scripts\activate`. Put the actual CSVs beside the scripts and run from Group_B. Datasets are not included.

| Assignment | Program | Required dataset |
|---|---|---|
| B1 Uber regression | b1_uber.py | uber.csv |
| B2 Spam KNN/SVM | b2_spam.py | emails.csv |
| B3 Churn neural network | b3_churn.py | Churn_Modelling.csv |
| B4 Diabetes KNN | b4_diabetes.py | diabetes.csv |
| B5 Sales clustering | b5_sales_clustering.py | sales_data_sample.csv |

Dataset download links and column requirements are in Group_B/Explanations.md. B5 displays the elbow plot: inspect it, close its window, then enter the chosen cluster count in the terminal. Scores are calculated from your actual files; no results are prefilled.

## Group C - Blockchain

| Assignment | File | How to use |
|---|---|---|
| C1 MetaMask installation and fees | c1_fee.py | Run with python3; supply transaction receipt values |
| C2 Wallet creation | c2_wallet.html | Browser wallet connection demo; create wallet in MetaMask first |
| C3 Bank contract | Bank.sol | Compile and deploy in Remix VM, then Sepolia if desired |
| C4 Student records | StudentRegistry.sol | Compile and deploy in Remix VM, then Sepolia if desired |

For C2, from Group_C run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://localhost:8000/c2_wallet.html in a browser with MetaMask enabled. Select Sepolia and click Connect. Stop the local server with Ctrl+C. The demo reads your public address and balance only. Wallet creation and the send/receive practical are completed inside MetaMask; see Explanations.md. It never asks for the recovery phrase.

For C3/C4 open https://remix.ethereum.org/ and import the .sol file. Use Solidity 0.8.20 or another compatible 0.8.x compiler. The contracts are not Python scripts; deployment and interaction require an Ethereum execution environment. Use Remix VM first, then test ETH only. Complete deployment/test steps and fee observation tables are in Group_C/Explanations.md.

## Validation and scope

Java syntax and Group A sample behavior are checked locally with OpenJDK javac/java. The ML workflows require the real CSVs and dependencies. The Solidity contracts require compilation and deployment in Remix. The MetaMask demo requires an installed, connected extension; no wallet transactions or deployments were performed when preparing these files.

Provider reference: https://docs.metamask.io/metamask-connect/evm/reference/json-rpc-api/eth_getBalance/
