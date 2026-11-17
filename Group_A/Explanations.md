# LP III - Group A
## Design and Analysis of Algorithms
SPPU | Fourth Year Computer Engineering | 2019 Course | 410246

Complete solutions for all six Group A assignments in the supplied LP III.pdf. Python 3 is used for clarity. Each code block is an independent program: save it using the indicated filename and run `python3 filename.py`. No third-party packages are required.

Examples below are expected results worked out from the supplied inputs, not claimed execution logs. Complexity uses the usual unit-cost arithmetic model; very large Python integers take extra bit-processing time.

## A1. Fibonacci numbers and step count
**Aim:** Generate the first n Fibonacci numbers and count execution steps.

**Idea:** Start with 0 and 1. Repeatedly output the current value and update the pair to (next, current + next). This avoids recomputing terms as naive recursion does.

**Counting convention:** Count each assignment, comparison, addition, append and return as one step. Tuple assignment counts as two assignments. The for-loop mechanism is not counted separately; the explicit while-loop condition is counted, including its final failed check. Function call and print overhead are excluded. There is no universal step count without such a convention.

### Code - a1_fibonacci.py
```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    # Counter bookkeeping itself is not part of the count.
    steps = 1             # n < 0 comparison
    a, b = 0, 1
    result = []
    i = 0
    steps += 4            # a, b, result, i assignments

    while i < n:
        steps += 1        # successful loop comparison
        result.append(a)
        steps += 1        # append
        a, b = b, a + b
        steps += 3        # addition, two assignments
        i = i + 1
        steps += 2        # addition and assignment

    steps += 1            # final failed comparison
    steps += 1            # return
    return result, steps


if __name__ == "__main__":
    n = int(input("Number of terms: "))
    terms, steps = fibonacci(n)
    print("Fibonacci:", terms)
    print("Counted steps:", steps)
    print("Formula 7n + 7:", 7 * n + 7)
```

**Walkthrough:** For n = 5, the pairs before output are (0,1), (1,1), (1,2), (2,3), (3,5), so the list is [0, 1, 1, 2, 3]. Counted steps = 42. For n = 0 the list is empty and steps = 7.

**Complexity:** Time O(n); O(n) space for the returned list, O(1) auxiliary state. Directly printing terms would avoid the list.

**Tell the examiner:** "I use two variables to store consecutive Fibonacci numbers. Every iteration generates one term, so runtime grows linearly with the number of terms. I define my step-count model explicitly, giving 7n + 7."

**Viva:** Why avoid naive recursion? It repeats the same subproblems and takes exponential time. Is this dynamic programming? It is the space-optimized iterative recurrence, retaining only the two necessary states.

## A2. Job sequencing with deadlines
**Aim:** Schedule unit-time jobs to maximize profit while meeting deadlines.

**Assumptions:** Each job takes exactly one time slot; one job runs per slot; profit is earned only if it finishes by its deadline. Deadlines are positive integers. Jobs are optional, so non-positive-profit jobs can be skipped.

**Algorithm:** Sort by decreasing profit. Put each job in the latest free slot on or before its deadline. Late placement keeps earlier slots available for more urgent jobs.

### Code - a2_job_sequencing.py
```python
def schedule_jobs(jobs):
    # A job is (name, deadline, profit).
    valid = [job for job in jobs if job[1] > 0 and job[2] > 0]
    if not valid:
        return [], 0

    horizon = min(len(valid), max(job[1] for job in valid))
    slots = [None] * horizon
    profit = 0
    for job in sorted(valid, key=lambda j: j[2], reverse=True):
        name, deadline, value = job
        for slot in range(min(deadline, horizon) - 1, -1, -1):
            if slots[slot] is None:
                slots[slot] = job
                profit += value
                break
    return slots, profit


if __name__ == "__main__":
    n = int(input("Number of jobs: "))
    jobs = []
    for i in range(n):
        entry = input(f"Job {i + 1} (ID Deadline Profit): ").strip().split()
        if len(entry) >= 3:
            name, deadline, profit = entry[0], int(entry[1]), int(entry[2])
        elif len(entry) == 2:
            name, deadline, profit = f"J{i + 1}", int(entry[0]), int(entry[1])
        elif len(entry) == 1:
            name = entry[0]
            deadline = int(input(f"  Deadline for {name}: "))
            profit = int(input(f"  Profit for {name}: "))
        else:
            name = f"J{i + 1}"
            deadline = int(input(f"  Deadline for Job {i + 1}: "))
            profit = int(input(f"  Profit for Job {i + 1}: "))
        jobs.append((name, deadline, profit))

    slots, profit = schedule_jobs(jobs)
    for time, job in enumerate(slots, start=1):
        print("Slot", time, ":", job[0] if job else "Idle")
    print("Maximum profit:", profit)
```

**Expected result:** Slots 1, 2 and 3 contain J3, J1 and J5. Total profit = 27 + 100 + 15 = 142. J1 is considered first but placed in slot 2.

**Explanation:** Sorting establishes the greedy choice. The inner reverse loop finds a feasible position. The break ensures each job is scheduled only once. Limiting the horizon to the number of valid jobs avoids allocating an unnecessarily large array.

**Complexity:** O(n log n + nD), where D = min(number of jobs, maximum deadline); worst case O(n²). O(n) space.

**Tell the examiner:** "I choose the highest-profit jobs first and assign each to the latest available slot before its deadline. This keeps earlier slots free while preserving feasibility."

**Viva:** Does this solve arbitrary-duration scheduling? No, the unit-duration assumption is essential. Why not schedule each selected job as early as possible? Doing so can block another job with a tighter deadline.

## A3. Fractional knapsack using greedy selection
**Aim:** Maximize value in a capacity-limited bag when fractions of items are allowed.

**Algorithm:** Compute value/weight, sort descending, take each item fully if possible, otherwise take only the fraction that fits.

### Code - a3_fractional_knapsack.py
```python
def fractional_knapsack(items, capacity):
    # Each item is (name, weight, value).
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    if any(w <= 0 or v < 0 for _, w, v in items):
        raise ValueError("Weights must be positive; values non-negative")

    total = 0.0
    chosen = []
    remaining = float(capacity)
    ordered = sorted(items, key=lambda item: item[2] / item[1],
                     reverse=True)
    for name, weight, value in ordered:
        if remaining <= 0:
            break
        taken_weight = min(weight, remaining)
        fraction = taken_weight / weight
        total += fraction * value
        remaining -= taken_weight
        chosen.append((name, fraction))
    return total, chosen


if __name__ == "__main__":
    n = int(input("Number of items: "))
    items = []
    for i in range(n):
        entry = input(f"Item {i + 1} (Name Weight Value): ").strip().split()
        if len(entry) >= 3:
            name, weight, value = entry[0], float(entry[1]), float(entry[2])
        elif len(entry) == 2:
            name = chr(ord('A') + i) if i < 26 else f"Item{i + 1}"
            weight, value = float(entry[0]), float(entry[1])
        elif len(entry) == 1:
            name = entry[0]
            weight = float(input(f"  Weight for {name}: "))
            value = float(input(f"  Value for {name}: "))
        else:
            name = chr(ord('A') + i) if i < 26 else f"Item{i + 1}"
            weight = float(input(f"  Weight for Item {i + 1}: "))
            value = float(input(f"  Value for Item {i + 1}: "))
        items.append((name, weight, value))

    capacity = float(input("Knapsack capacity: "))
    value, chosen = fractional_knapsack(items, capacity)
    for name, fraction in chosen:
        print(name, "fraction =", round(fraction, 4))
    print("Maximum value:", round(value, 2))
```

**Expected result:** A = 1.0, B = 1.0, C = 0.6667; value = 240.00. Ratios are 6, 5 and 4. After A and B, 20 units remain, so take 20/30 of C, contributing 80.

**Complexity:** O(n log n) time due to sorting; O(n) space for sorted items and the result.

**Tell the examiner:** "Because items are divisible, every unit of capacity should be filled with the highest available value per unit weight. The final selected item may be fractional."

**Viva:** Why does this fail for 0-1 knapsack? Indivisibility means a high-ratio item can prevent a better combination. For these same items, the 0-1 optimum is B + C = 220, while ratio-greedy would choose A + B = 160.

## A4. 0-1 knapsack using dynamic programming
**Aim:** Select whole items to maximize value without exceeding capacity. Each item can be selected once.

**State:** dp[i][c] = maximum value using the first i items within capacity c.
If weight w of item i exceeds c, copy the previous answer. Otherwise choose the better of excluding the item and including it: max(dp[i-1][c], value + dp[i-1][c-w]).

### Code - a4_zero_one_knapsack.py
```python
def knapsack(weights, values, capacity):
    if len(weights) != len(values):
        raise ValueError("Lengths must match")
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("Capacity must be a non-negative integer")
    if any(not isinstance(w, int) or w <= 0 for w in weights):
        raise ValueError("Weights must be positive integers")

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, value = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(
                    dp[i][c], value + dp[i - 1][c - w]
                )

    selected = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(i - 1)
            c -= weights[i - 1]
    selected.reverse()
    return dp[n][capacity], selected


if __name__ == "__main__":
    n = int(input("Number of items: "))
    weights = []
    values = []
    for i in range(n):
        entry = input(f"Item {i + 1} (Weight Value): ").strip().split()
        if len(entry) >= 2:
            w, v = int(entry[0]), int(entry[1])
        elif len(entry) == 1:
            w = int(entry[0])
            v = int(input(f"  Value for Item {i + 1}: "))
        else:
            w = int(input(f"  Weight for Item {i + 1}: "))
            v = int(input(f"  Value for Item {i + 1}: "))
        weights.append(w)
        values.append(v)

    capacity = int(input("Knapsack capacity: "))
    best, selected = knapsack(weights, values, capacity)
    print("Maximum value:", best)
    print("Selected item numbers:", [i + 1 for i in selected])
```

**Expected result:** Maximum value 220; selected item numbers [2, 3].

**Explanation:** Row 0 represents no items. Referring to the previous row in both choices prevents reusing the same item. Backtracking through changed cells recovers one optimum; ties may allow several valid solutions.

**Complexity:** O(nW) time and space, where W is integer capacity. This is pseudo-polynomial because W's numeric value, rather than its bit length, appears in the complexity. A one-dimensional array reduces memory to O(W), but recovering selected items needs additional care.

**Tell the examiner:** "For each item and capacity I compare include and exclude choices, store the optimum, and reuse smaller answers. Unlike fractional knapsack, I never take part of an item."

**Viva:** Why dynamic programming? The problem has optimal substructure and overlapping subproblems. In a one-dimensional implementation, why traverse capacities backwards? To avoid using the current item more than once.

## A5. Binomial coefficients using dynamic programming
**Aim:** Generate Pascal's triangle and obtain C(n,r).

**Recurrence:** C(n,0) = C(n,n) = 1; C(n,r) = C(n-1,r-1) + C(n-1,r). The recurrence counts selections that include a chosen element and selections that exclude it.

### Code - a5_binomial.py
```python
def binomial_table(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    table = []
    for i in range(n + 1):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = table[i - 1][j - 1] + table[i - 1][j]
        table.append(row)
    return table


if __name__ == "__main__":
    n = int(input("n: "))
    r = int(input("r: "))
    if not 0 <= r <= n:
        raise ValueError("Require 0 <= r <= n")
    table = binomial_table(n)
    for row in table:
        print(*row)
    print("C(n, r) =", table[n][r])
```

**Example:** n = 5, r = 2 gives final row 1 5 10 10 5 1 and C(5,2) = 10. Row 0 is [1].

**Complexity:** O(n²) time and space for the whole triangle. Computing only C(n,r) can use O(nr) time and O(r) memory by updating one row backwards.

**Tell the examiner:** "Every inner coefficient is the sum of the two coefficients above it. I store previously computed rows, avoiding repeated recursive work and factorial calculations."

**Viva:** What is C(n,r)? The number of ways to choose r objects from n without considering order. Why are the edges 1? There is one way to choose nothing and one way to choose all objects.

## A6. Eight queens with a fixed first queen
**Aim:** Place eight queens so no two share a row, column or diagonal, preserving the supplied queen.

**Input convention:** Enter the fixed queen's row and column from 1 to 8. It can be anywhere, not only in the top-left cell. Internally rows and columns are indexed 0 to 7.

**Algorithm:** Mark the fixed queen's column and both diagonals as occupied. Recursively place one queen in every other row. If a row has no safe column, undo the previous choice and try another.

### Code - a6_eight_queens.py
```python
def solve_queens(fixed_row, fixed_col, n=8):
    if not (0 <= fixed_row < n and 0 <= fixed_col < n):
        raise ValueError("Fixed queen is outside the board")

    board = [-1] * n
    board[fixed_row] = fixed_col
    columns = {fixed_col}
    down_diagonals = {fixed_row - fixed_col}
    up_diagonals = {fixed_row + fixed_col}

    def place(row):
        if row == n:
            return True
        if row == fixed_row:
            return place(row + 1)

        for col in range(n):
            d1, d2 = row - col, row + col
            if (col in columns or d1 in down_diagonals
                    or d2 in up_diagonals):
                continue
            board[row] = col
            columns.add(col)
            down_diagonals.add(d1)
            up_diagonals.add(d2)
            if place(row + 1):
                return True
            board[row] = -1
            columns.remove(col)
            down_diagonals.remove(d1)
            up_diagonals.remove(d2)
        return False

    return board if place(0) else None


if __name__ == "__main__":
    row = int(input("Fixed queen row (1-8): ")) - 1
    col = int(input("Fixed queen column (1-8): ")) - 1
    answer = solve_queens(row, col)
    if answer is None:
        print("No solution")
    else:
        for queen_col in answer:
            print(*[int(c == queen_col) for c in range(8)])
        print("Queen columns (1-based):",
              [c + 1 for c in answer])
```

**Example:** With fixed queen at (1,1), a valid solution has queen columns [1,5,8,6,3,7,2,4]. Each row contains exactly one 1. Column values, row-column values and row+column values must each be unique.

**Explanation:** Equal row-column values indicate one diagonal direction; equal row+column values indicate the other. The sets include the fixed queen before recursion, so earlier rows cannot accidentally attack it. Removing set entries implements backtracking. This program stops after finding one solution.

**Complexity:** For generalized N queens, a conservative bound for this implementation is O(N × N!) time because each recursive state scans N columns. Search is commonly summarized as factorial; pruning improves actual runtime. O(N) auxiliary state and recursion stack, excluding printed output.

**Tell the examiner:** "I place one queen per row, check columns and diagonals, and undo placements that lead to dead ends. The given queen is marked in advance and never moved."

**Viva:** Why not greedy? A safe placement now can prevent completion later. How to find all solutions? Record the board at the base case and continue searching instead of returning immediately.

## Practical revision
1. Greedy makes an irrevocable local choice: job sequencing and fractional knapsack.
2. Dynamic programming stores subproblem answers: 0-1 knapsack and binomial coefficients.
3. Backtracking explores alternatives and reverses failed choices: eight queens.
4. Always state assumptions before claiming complexity or optimality.

**Source:** Assignment numbering and scope follow the supplied SPPU LP III.pdf, Group A. These are explanatory reference implementations.

