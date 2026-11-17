#!/usr/bin/env python3
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_test(title, cmd, cwd, stdin_data=None, env_vars=None):
    print("=" * 70)
    print(f"▶ RUNNING: {title}")
    print(f"  Command: {' '.join(cmd)}")
    print(f"  Working Dir: {cwd}")
    if stdin_data:
        print(f"  Input: {repr(stdin_data.strip())}")
    print("-" * 70)

    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"  # Prevent GUI plot windows from blocking
    if env_vars:
        env.update(env_vars)

    res = subprocess.run(
        cmd,
        cwd=cwd,
        input=stdin_data,
        text=True,
        capture_output=True,
        env=env
    )

    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        # Filter benign matplotlib and sklearn warnings if needed or display them
        lines = [line for line in res.stderr.splitlines() if "UserWarning: FigureCanvasAgg" not in line]
        if lines:
            print("\n[Stderr / Warnings]:")
            print("\n".join(lines[:10]))
            if len(lines) > 10:
                print(f"... and {len(lines) - 10} more warning lines")

    status = "SUCCESS" if res.returncode == 0 else f"FAILED (exit code {res.returncode})"
    print(f"\nResult: [{status}]")
    print("=" * 70 + "\n")
    return res.returncode == 0

def main():
    results = {}
    python_exe = sys.executable

    print("\n" + "#" * 70)
    print("# RUNNING GROUP A: ALGORITHMS (Python)")
    print("#" * 70 + "\n")

    group_a_dir = os.path.join(BASE_DIR, "Group_A")
    results["A1 - Fibonacci (n=10)"] = run_test(
        "A1 Fibonacci", [python_exe, "a1_fibonacci.py"], group_a_dir, stdin_data="10\n"
    )
    results["A2 - Job Sequencing"] = run_test(
        "A2 Job Sequencing", [python_exe, "a2_job_sequencing.py"], group_a_dir,
        stdin_data="5\nJ1 2 100\nJ2 1 19\nJ3 2 27\nJ4 1 25\nJ5 3 15\n"
    )
    results["A3 - Fractional Knapsack"] = run_test(
        "A3 Fractional Knapsack", [python_exe, "a3_fractional_knapsack.py"], group_a_dir,
        stdin_data="3\nA 10 60\nB 20 100\nC 30 120\n50\n"
    )
    results["A4 - 0/1 Knapsack"] = run_test(
        "A4 0/1 Knapsack", [python_exe, "a4_zero_one_knapsack.py"], group_a_dir,
        stdin_data="3\n10 60\n20 100\n30 120\n50\n"
    )
    results["A5 - Binomial Coefficients (n=5, r=2)"] = run_test(
        "A5 Binomial Coefficients", [python_exe, "a5_binomial.py"], group_a_dir, stdin_data="5\n2\n"
    )
    results["A6 - Eight Queens (row=1, col=1)"] = run_test(
        "A6 Eight Queens", [python_exe, "a6_eight_queens.py"], group_a_dir, stdin_data="1\n1\n"
    )

    print("\n" + "#" * 70)
    print("# RUNNING GROUP B: MACHINE LEARNING")
    print("#" * 70 + "\n")

    group_b_dir = os.path.join(BASE_DIR, "Group_B")
    results["B1 - Uber Regression"] = run_test(
        "B1 Uber Regression", [python_exe, "b1_uber.py"], group_b_dir
    )
    results["B2 - Spam Classification (KNN & SVM)"] = run_test(
        "B2 Spam Classification", [python_exe, "b2_spam.py"], group_b_dir
    )
    results["B3 - Churn Prediction (MLP Classifier)"] = run_test(
        "B3 Churn Neural Network", [python_exe, "b3_churn.py"], group_b_dir
    )
    results["B4 - Diabetes (KNN)"] = run_test(
        "B4 Diabetes KNN", [python_exe, "b4_diabetes.py"], group_b_dir
    )
    results["B5 - Sales Clustering (K-Means, k=3)"] = run_test(
        "B5 Sales Clustering", [python_exe, "b5_sales_clustering.py"], group_b_dir, stdin_data="3\n"
    )

    print("\n" + "#" * 70)
    print("# RUNNING GROUP C: BLOCKCHAIN")
    print("#" * 70 + "\n")

    group_c_dir = os.path.join(BASE_DIR, "Group_C")
    results["C1 - Fee Calculation"] = run_test(
        "C1 Transaction Fee", [python_exe, "c1_fee.py"], group_c_dir, stdin_data="21000\n20\n0.05\n"
    )

    # Compile Solidity contracts with npx solc
    results["C3 - Bank.sol Compilation"] = run_test(
        "C3 Bank Contract Compilation", ["npx", "--yes", "solc", "--bin", "--abi", "Bank.sol"], group_c_dir
    )
    results["C4 - StudentRegistry.sol Compilation"] = run_test(
        "C4 Student Registry Contract Compilation", ["npx", "--yes", "solc", "--bin", "--abi", "StudentRegistry.sol"], group_c_dir
    )

    print("\n" + "#" * 70)
    print("# EXECUTION SUMMARY REPORT")
    print("#" * 70)
    all_passed = True
    for name, success in results.items():
        status = "PASSED" if success else "FAILED"
        print(f"  {name:<48} : {status}")
        if not success:
            all_passed = False

    print("#" * 70)
    if all_passed:
        print("🎉 ALL 13 EXECUTABLE FILES & CONTRACTS RAN SUCCESSFULLY!")
    else:
        print("⚠️ Some files failed. Please check the logs above.")
    print("#" * 70 + "\n")

if __name__ == "__main__":
    main()
