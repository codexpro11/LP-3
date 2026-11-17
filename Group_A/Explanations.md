# LP III - Group A
## Design and Analysis of Algorithms
SPPU | Fourth Year Computer Engineering | 2019 Course | 410246

Complete solutions for all six Group A assignments in the supplied LP III.pdf. Java is used for implementation. Each code file is an independent program: compile and run using `javac FileName.java && java ClassName` or run directly using `java FileName.java`. No third-party packages are required (uses standard `java.util`).

Examples below are expected results worked out from the supplied inputs. Complexity uses the standard unit-cost arithmetic model.

---

## A1. Fibonacci numbers and step count
**Aim:** Generate the first n Fibonacci numbers and count execution steps.

**Idea:** Start with 0 and 1. Repeatedly output the current value and update the pair to (next, current + next). This avoids recomputing terms as naive recursion does.

**Counting convention:** Count each assignment, comparison, addition, append/add, and return as one step. The for/while loop mechanism counts the explicit comparison in each iteration including the final failed check. Function call and print overhead are excluded. There is no universal step count without such an explicit convention.

### Code - A1_Fibonacci.java
```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class A1_Fibonacci {
    public static class Result {
        public final List<Long> terms;
        public final long steps;

        public Result(List<Long> terms, long steps) {
            this.terms = terms;
            this.steps = steps;
        }
    }

    public static Result fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }

        // Counter bookkeeping itself is not part of the count.
        long steps = 1; // n < 0 comparison
        long a = 0, b = 1;
        List<Long> result = new ArrayList<>();
        int i = 0;
        steps += 4; // a, b, result, i assignments

        while (i < n) {
            steps += 1; // successful loop comparison
            result.add(a);
            steps += 1; // append / add
            long temp = a + b;
            a = b;
            b = temp;
            steps += 3; // addition, two assignments
            i = i + 1;
            steps += 2; // addition and assignment
        }

        steps += 1; // final failed comparison
        steps += 1; // return
        return new Result(result, steps);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of terms: ");
        if (!scanner.hasNextInt()) {
            System.err.println("Invalid input. Non-negative integer required.");
            return;
        }
        int n = scanner.nextInt();
        Result res = fibonacci(n);
        System.out.println("Fibonacci: " + res.terms);
        System.out.println("Counted steps: " + res.steps);
        System.out.println("Formula 7n + 7: " + (7L * n + 7));
    }
}
```

**Walkthrough:** For n = 5, the pairs before output are (0,1), (1,1), (1,2), (2,3), (3,5), so the list is [0, 1, 1, 2, 3]. Counted steps = 42. For n = 0 the list is empty and steps = 7.

**Complexity:** Time O(n); O(n) space for the returned list, O(1) auxiliary state.

**Tell the examiner:** "I use two variables to store consecutive Fibonacci numbers. Every iteration generates one term, so runtime grows linearly with the number of terms. I define my step-count model explicitly, giving 7n + 7."

**Viva:** Why avoid naive recursion? It repeats the same subproblems and takes exponential time ($O(2^n)$). Is this dynamic programming? It is the space-optimized iterative recurrence, retaining only the two necessary states.

---

## A2. Job sequencing with deadlines
**Aim:** Schedule unit-time jobs to maximize profit while meeting deadlines.

**Assumptions:** Each job takes exactly one time slot; one job runs per slot; profit is earned only if it finishes by its deadline. Deadlines are positive integers. Jobs are optional, so non-positive-profit jobs can be skipped.

**Algorithm:** Sort by decreasing profit. Put each job in the latest free slot on or before its deadline. Late placement keeps earlier slots available for more urgent jobs.

### Code - A2_JobSequencing.java
```java
import java.util.*;

public class A2_JobSequencing {
    public static class Job {
        public String id;
        public int deadline;
        public int profit;

        public Job(String id, int deadline, int profit) {
            this.id = id;
            this.deadline = deadline;
            this.profit = profit;
        }
    }

    public static class ScheduleResult {
        public Job[] slots;
        public int totalProfit;

        public ScheduleResult(Job[] slots, int totalProfit) {
            this.slots = slots;
            this.totalProfit = totalProfit;
        }
    }

    public static ScheduleResult scheduleJobs(List<Job> jobs) {
        List<Job> valid = new ArrayList<>();
        int maxDeadline = 0;
        for (Job j : jobs) {
            if (j.deadline > 0 && j.profit > 0) {
                valid.add(j);
                if (j.deadline > maxDeadline) {
                    maxDeadline = j.deadline;
                }
            }
        }
        if (valid.isEmpty()) {
            return new ScheduleResult(new Job[0], 0);
        }

        int horizon = Math.min(valid.size(), maxDeadline);
        Job[] slots = new Job[horizon];
        int totalProfit = 0;

        // Sort descending by profit
        valid.sort((a, b) -> Integer.compare(b.profit, a.profit));

        for (Job job : valid) {
            int maxSlot = Math.min(job.deadline, horizon) - 1;
            for (int s = maxSlot; s >= 0; s--) {
                if (slots[s] == null) {
                    slots[s] = job;
                    totalProfit += job.profit;
                    break;
                }
            }
        }

        return new ScheduleResult(slots, totalProfit);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of jobs: ");
        if (!scanner.hasNextInt()) return;
        int n = scanner.nextInt();
        scanner.nextLine();

        List<Job> jobs = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            System.out.print("Job " + (i + 1) + " (ID Deadline Profit): ");
            String line = "";
            while (line.isEmpty() && scanner.hasNextLine()) {
                line = scanner.nextLine().trim();
            }
            String[] parts = line.split("\\s+");
            String id;
            int deadline;
            int profit;

            if (parts.length >= 3) {
                id = parts[0];
                deadline = Integer.parseInt(parts[1]);
                profit = Integer.parseInt(parts[2]);
            } else if (parts.length == 2) {
                id = "J" + (i + 1);
                deadline = Integer.parseInt(parts[0]);
                profit = Integer.parseInt(parts[1]);
            } else if (parts.length == 1 && !parts[0].isEmpty()) {
                id = parts[0];
                System.out.print("  Deadline for " + id + ": ");
                deadline = scanner.nextInt();
                System.out.print("  Profit for " + id + ": ");
                profit = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            } else {
                id = "J" + (i + 1);
                System.out.print("  Deadline for Job " + (i + 1) + ": ");
                deadline = scanner.nextInt();
                System.out.print("  Profit for Job " + (i + 1) + ": ");
                profit = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            }
            jobs.add(new Job(id, deadline, profit));
        }

        ScheduleResult result = scheduleJobs(jobs);
        for (int time = 0; time < result.slots.length; time++) {
            Job job = result.slots[time];
            System.out.println("Slot " + (time + 1) + " : " + (job != null ? job.id : "Idle"));
        }
        System.out.println("Maximum profit: " + result.totalProfit);
    }
}
```

**Expected result:** With 5 jobs (`J1 2 100`, `J2 1 19`, `J3 2 27`, `J4 1 25`, `J5 3 15`), Slots 1, 2 and 3 contain J3, J1 and J5. Total profit = 27 + 100 + 15 = 142. J1 is considered first but placed in slot 2.

**Explanation:** Sorting establishes the greedy choice. The inner reverse loop finds a feasible position. The break ensures each job is scheduled only once. Limiting the horizon to the number of valid jobs avoids allocating an unnecessarily large array.

**Complexity:** O(n log n + nD), where D = min(number of jobs, maximum deadline); worst case O(n²). O(n) space.

**Tell the examiner:** "I choose the highest-profit jobs first and assign each to the latest available slot before its deadline. This keeps earlier slots free while preserving feasibility."

**Viva:** Does this solve arbitrary-duration scheduling? No, the unit-duration assumption is essential. Why not schedule each selected job as early as possible? Doing so can block another job with a tighter deadline.

---

## A3. Fractional knapsack using greedy selection
**Aim:** Maximize value in a capacity-limited bag when fractions of items are allowed.

**Algorithm:** Compute value/weight, sort descending, take each item fully if possible, otherwise take only the fraction that fits.

### Code - A3_FractionalKnapsack.java
```java
import java.util.*;

public class A3_FractionalKnapsack {
    public static class Item {
        public String name;
        public double weight;
        public double value;

        public Item(String name, double weight, double value) {
            this.name = name;
            this.weight = weight;
            this.value = value;
        }

        public double ratio() {
            return value / weight;
        }
    }

    public static class SelectedItem {
        public String name;
        public double fraction;

        public SelectedItem(String name, double fraction) {
            this.name = name;
            this.fraction = fraction;
        }
    }

    public static class Result {
        public double totalValue;
        public List<SelectedItem> chosen;

        public Result(double totalValue, List<SelectedItem> chosen) {
            this.totalValue = totalValue;
            this.chosen = chosen;
        }
    }

    public static Result fractionalKnapsack(List<Item> items, double capacity) {
        if (capacity < 0) {
            throw new IllegalArgumentException("Capacity cannot be negative");
        }
        for (Item item : items) {
            if (item.weight <= 0 || item.value < 0) {
                throw new IllegalArgumentException("Weights must be positive; values non-negative");
            }
        }

        List<Item> ordered = new ArrayList<>(items);
        ordered.sort((a, b) -> Double.compare(b.ratio(), a.ratio()));

        double total = 0.0;
        double remaining = capacity;
        List<SelectedItem> chosen = new ArrayList<>();

        for (Item item : ordered) {
            if (remaining <= 0) break;
            double takenWeight = Math.min(item.weight, remaining);
            double fraction = takenWeight / item.weight;
            total += fraction * item.value;
            remaining -= takenWeight;
            chosen.add(new SelectedItem(item.name, fraction));
        }

        return new Result(total, chosen);
    }

    private static String formatFraction(double fraction) {
        double rounded = Math.round(fraction * 10000.0) / 10000.0;
        if (rounded == (long) rounded) {
            return String.format(Locale.US, "%.1f", rounded);
        }
        return String.valueOf(rounded);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of items: ");
        if (!scanner.hasNextInt()) return;
        int n = scanner.nextInt();
        scanner.nextLine();

        List<Item> items = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            System.out.print("Item " + (i + 1) + " (Name Weight Value): ");
            String line = "";
            while (line.isEmpty() && scanner.hasNextLine()) {
                line = scanner.nextLine().trim();
            }
            String[] parts = line.split("\\s+");
            String name;
            double weight;
            double value;

            if (parts.length >= 3) {
                name = parts[0];
                weight = Double.parseDouble(parts[1]);
                value = Double.parseDouble(parts[2]);
            } else if (parts.length == 2) {
                name = (i < 26) ? String.valueOf((char) ('A' + i)) : ("Item" + (i + 1));
                weight = Double.parseDouble(parts[0]);
                value = Double.parseDouble(parts[1]);
            } else if (parts.length == 1 && !parts[0].isEmpty()) {
                name = parts[0];
                System.out.print("  Weight for " + name + ": ");
                weight = scanner.nextDouble();
                System.out.print("  Value for " + name + ": ");
                value = scanner.nextDouble();
                if (scanner.hasNextLine()) scanner.nextLine();
            } else {
                name = (i < 26) ? String.valueOf((char) ('A' + i)) : ("Item" + (i + 1));
                System.out.print("  Weight for Item " + (i + 1) + ": ");
                weight = scanner.nextDouble();
                System.out.print("  Value for Item " + (i + 1) + ": ");
                value = scanner.nextDouble();
                if (scanner.hasNextLine()) scanner.nextLine();
            }
            items.add(new Item(name, weight, value));
        }

        System.out.print("Knapsack capacity: ");
        if (!scanner.hasNextDouble()) return;
        double capacity = scanner.nextDouble();

        Result result = fractionalKnapsack(items, capacity);
        for (SelectedItem item : result.chosen) {
            System.out.println(item.name + " fraction = " + formatFraction(item.fraction));
        }
        System.out.printf(Locale.US, "Maximum value: %.2f%n", result.totalValue);
    }
}
```

**Expected result:** For items `A 10 60`, `B 20 100`, `C 30 120` and capacity `50`: A = 1.0, B = 1.0, C = 0.6667; Maximum value = 240.00. Ratios are 6, 5 and 4. After A and B, 20 units remain, taking 20/30 of C (adding 80).

**Complexity:** O(n log n) time due to sorting; O(n) space for sorted items and the result.

**Tell the examiner:** "Because items are divisible, every unit of capacity should be filled with the highest available value per unit weight. The final selected item may be fractional."

**Viva:** Why does this fail for 0-1 knapsack? Indivisibility means a high-ratio item can prevent a better combination. For these same items, the 0-1 optimum is B + C = 220, while ratio-greedy would choose A + B = 160.

---

## A4. 0-1 knapsack using dynamic programming
**Aim:** Select whole items to maximize value without exceeding capacity. Each item can be selected once.

**State:** dp[i][c] = maximum value using the first i items within capacity c.
If weight w of item i exceeds c, copy the previous answer. Otherwise choose the better of excluding the item and including it: max(dp[i-1][c], value + dp[i-1][c-w]).

### Code - A4_ZeroOneKnapsack.java
```java
import java.util.*;

public class A4_ZeroOneKnapsack {
    public static class Result {
        public int maxValue;
        public List<Integer> selectedItems;

        public Result(int maxValue, List<Integer> selectedItems) {
            this.maxValue = maxValue;
            this.selectedItems = selectedItems;
        }
    }

    public static Result knapsack(int[] weights, int[] values, int capacity) {
        if (weights.length != values.length) {
            throw new IllegalArgumentException("Lengths must match");
        }
        if (capacity < 0) {
            throw new IllegalArgumentException("Capacity must be a non-negative integer");
        }
        for (int w : weights) {
            if (w <= 0) {
                throw new IllegalArgumentException("Weights must be positive integers");
            }
        }

        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];

        for (int i = 1; i <= n; i++) {
            int w = weights[i - 1];
            int value = values[i - 1];
            for (int c = 0; c <= capacity; c++) {
                dp[i][c] = dp[i - 1][c];
                if (w <= c) {
                    dp[i][c] = Math.max(dp[i][c], value + dp[i - 1][c - w]);
                }
            }
        }

        List<Integer> selected = new ArrayList<>();
        int c = capacity;
        for (int i = n; i > 0; i--) {
            if (dp[i][c] != dp[i - 1][c]) {
                selected.add(i); // 1-based index
                c -= weights[i - 1];
            }
        }
        Collections.reverse(selected);

        return new Result(dp[n][capacity], selected);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of items: ");
        if (!scanner.hasNextInt()) return;
        int n = scanner.nextInt();
        scanner.nextLine();

        int[] weights = new int[n];
        int[] values = new int[n];

        for (int i = 0; i < n; i++) {
            System.out.print("Item " + (i + 1) + " (Weight Value): ");
            String line = "";
            while (line.isEmpty() && scanner.hasNextLine()) {
                line = scanner.nextLine().trim();
            }
            String[] parts = line.split("\\s+");
            if (parts.length >= 2) {
                weights[i] = Integer.parseInt(parts[0]);
                values[i] = Integer.parseInt(parts[1]);
            } else if (parts.length == 1 && !parts[0].isEmpty()) {
                weights[i] = Integer.parseInt(parts[0]);
                System.out.print("  Value for Item " + (i + 1) + ": ");
                values[i] = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            } else {
                System.out.print("  Weight for Item " + (i + 1) + ": ");
                weights[i] = scanner.nextInt();
                System.out.print("  Value for Item " + (i + 1) + ": ");
                values[i] = scanner.nextInt();
                if (scanner.hasNextLine()) scanner.nextLine();
            }
        }

        System.out.print("Knapsack capacity: ");
        if (!scanner.hasNextInt()) return;
        int capacity = scanner.nextInt();

        Result res = knapsack(weights, values, capacity);
        System.out.println("Maximum value: " + res.maxValue);
        System.out.println("Selected item numbers: " + res.selectedItems);
    }
}
```

**Expected result:** For weights `[10, 20, 30]`, values `[60, 100, 120]`, capacity `50`: Maximum value 220; selected item numbers [2, 3].

**Explanation:** Row 0 represents no items. Referring to the previous row in both choices prevents reusing the same item. Backtracking through changed cells recovers one optimum; ties may allow several valid solutions.

**Complexity:** O(nW) time and space, where W is integer capacity. This is pseudo-polynomial because W's numeric value, rather than its bit length, appears in the complexity.

**Tell the examiner:** "For each item and capacity I compare include and exclude choices, store the optimum, and reuse smaller answers. Unlike fractional knapsack, I never take part of an item."

**Viva:** Why dynamic programming? The problem has optimal substructure and overlapping subproblems. In a one-dimensional implementation, why traverse capacities backwards? To avoid using the current item more than once.

---

## A5. Binomial coefficients using dynamic programming
**Aim:** Generate Pascal's triangle and obtain C(n,r).

**Recurrence:** C(n,0) = C(n,n) = 1; C(n,r) = C(n-1,r-1) + C(n-1,r). The recurrence counts selections that include a chosen element and selections that exclude it.

### Code - A5_Binomial.java
```java
import java.util.Scanner;

public class A5_Binomial {
    public static long[][] binomialTable(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }
        long[][] table = new long[n + 1][];
        for (int i = 0; i <= n; i++) {
            table[i] = new long[i + 1];
            table[i][0] = 1;
            table[i][i] = 1;
            for (int j = 1; j < i; j++) {
                table[i][j] = table[i - 1][j - 1] + table[i - 1][j];
            }
        }
        return table;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("n: ");
        if (!scanner.hasNextInt()) return;
        int n = scanner.nextInt();

        System.out.print("r: ");
        if (!scanner.hasNextInt()) return;
        int r = scanner.nextInt();

        if (r < 0 || r > n) {
            throw new IllegalArgumentException("Require 0 <= r <= n");
        }

        long[][] table = binomialTable(n);
        for (int i = 0; i <= n; i++) {
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j <= i; j++) {
                if (j > 0) sb.append(" ");
                sb.append(table[i][j]);
            }
            System.out.println(sb.toString());
        }
        System.out.println("C(n, r) = " + table[n][r]);
    }
}
```

**Example:** n = 5, r = 2 gives final row `1 5 10 10 5 1` and `C(5, 2) = 10`.

**Complexity:** O(n²) time and space for the whole triangle.

**Tell the examiner:** "Every inner coefficient is the sum of the two coefficients above it. I store previously computed rows, avoiding repeated recursive work and factorial calculations."

**Viva:** What is C(n,r)? The number of ways to choose r objects from n without considering order. Why are the edges 1? There is one way to choose nothing and one way to choose all objects.

---

## A6. Eight queens with a fixed first queen
**Aim:** Place eight queens so no two share a row, column or diagonal, preserving the supplied queen.

**Input convention:** Enter the fixed queen's row and column from 1 to 8. Internally rows and columns are indexed 0 to 7.

**Algorithm:** Mark the fixed queen's column and both diagonals as occupied. Recursively place one queen in every other row. If a row has no safe column, undo the previous choice and backtrack.

### Code - A6_EightQueens.java
```java
import java.util.*;

public class A6_EightQueens {
    public static int[] solveQueens(int fixedRow, int fixedCol, int n) {
        if (fixedRow < 0 || fixedRow >= n || fixedCol < 0 || fixedCol >= n) {
            throw new IllegalArgumentException("Fixed queen is outside the board");
        }

        int[] board = new int[n];
        Arrays.fill(board, -1);
        board[fixedRow] = fixedCol;

        Set<Integer> columns = new HashSet<>();
        Set<Integer> downDiagonals = new HashSet<>();
        Set<Integer> upDiagonals = new HashSet<>();

        columns.add(fixedCol);
        downDiagonals.add(fixedRow - fixedCol);
        upDiagonals.add(fixedRow + fixedCol);

        boolean solved = place(0, n, fixedRow, board, columns, downDiagonals, upDiagonals);
        return solved ? board : null;
    }

    private static boolean place(int row, int n, int fixedRow, int[] board,
                                 Set<Integer> columns, Set<Integer> downDiagonals, Set<Integer> upDiagonals) {
        if (row == n) {
            return true;
        }
        if (row == fixedRow) {
            return place(row + 1, n, fixedRow, board, columns, downDiagonals, upDiagonals);
        }

        for (int col = 0; col < n; col++) {
            int d1 = row - col;
            int d2 = row + col;
            if (columns.contains(col) || downDiagonals.contains(d1) || upDiagonals.contains(d2)) {
                continue;
            }

            board[row] = col;
            columns.add(col);
            downDiagonals.add(d1);
            upDiagonals.add(d2);

            if (place(row + 1, n, fixedRow, board, columns, downDiagonals, upDiagonals)) {
                return true;
            }

            board[row] = -1;
            columns.remove(col);
            downDiagonals.remove(d1);
            upDiagonals.remove(d2);
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Fixed queen row (1-8): ");
        if (!scanner.hasNextInt()) return;
        int row = scanner.nextInt() - 1;

        System.out.print("Fixed queen column (1-8): ");
        if (!scanner.hasNextInt()) return;
        int col = scanner.nextInt() - 1;

        int[] answer = solveQueens(row, col, 8);
        if (answer == null) {
            System.out.println("No solution");
        } else {
            for (int queenCol : answer) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 8; c++) {
                    if (c > 0) sb.append(" ");
                    sb.append(c == queenCol ? 1 : 0);
                }
                System.out.println(sb.toString());
            }

            List<Integer> cols1Based = new ArrayList<>();
            for (int c : answer) {
                cols1Based.add(c + 1);
            }
            System.out.println("Queen columns (1-based): " + cols1Based);
        }
    }
}
```

**Example:** With fixed queen at (1,1), a valid solution has queen columns `[1, 5, 8, 6, 3, 7, 2, 4]`. Each row contains exactly one 1.

**Complexity:** O(N × N!) time in the worst case; O(N) auxiliary state and recursion stack.

---

## Practical revision
1. Greedy makes an irrevocable local choice: job sequencing and fractional knapsack.
2. Dynamic programming stores subproblem answers: 0-1 knapsack and binomial coefficients.
3. Backtracking explores alternatives and reverses failed choices: eight queens.
4. Always state assumptions before claiming complexity or optimality.

**Source:** Assignment numbering and scope follow the supplied SPPU LP III.pdf, Group A.
