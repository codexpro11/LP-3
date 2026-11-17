# LP III - Group A
## Design and Analysis of Algorithms
SPPU | Fourth Year Computer Engineering | 2019 Course | 410246

Complete solutions for all six Group A assignments in the supplied LP III.pdf. Java is used for implementation. Each code file is an independent program: compile and run using `javac FileName.java && java ClassName` or run directly using `java FileName.java`. No third-party packages are required (uses standard `java.util`).

Examples below are expected results worked out from the supplied inputs. Complexity uses the standard unit-cost arithmetic model.

---

## A1. Fibonacci numbers
**Aim:** Generate the first n Fibonacci numbers.

**Idea:** Start with 0 and 1. Repeatedly output the current value and update the pair to (next, current + next). This avoids recomputing terms as naive recursion does.

### Code - A1_Fibonacci.java
```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class A1_Fibonacci {
    public static List<Long> fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }

        List<Long> result = new ArrayList<>();
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            result.add(a);
            long temp = a + b;
            a = b;
            b = temp;
        }

        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of terms: ");
        if (!scanner.hasNextInt()) {
            System.err.println("Invalid input. Non-negative integer required.");
            return;
        }
        int n = scanner.nextInt();
        List<Long> terms = fibonacci(n);
        System.out.println("Fibonacci: " + terms);
    }
}
```

**Walkthrough:** For n = 5, the pairs before output are (0,1), (1,1), (1,2), (2,3), (3,5), so the list is [0, 1, 1, 2, 3]. For n = 0 the list is empty.

**Complexity:** Time O(n); O(n) space for the returned list, O(1) auxiliary state.

**Tell the examiner:** "I use two variables to store consecutive Fibonacci numbers. Every iteration generates one term, so runtime grows linearly with the number of terms."

**Viva:** Why avoid naive recursion? It repeats the same subproblems and takes exponential time ($O(2^n)$). Is this dynamic programming? It is the space-optimized iterative recurrence, retaining only the two necessary states.

---

## A2. Huffman Encoding using Greedy Strategy
**Aim:** Write a program to implement Huffman Encoding using a greedy strategy.

**Objective:** Understand and solve Huffman Encoding using the greedy method for lossless data compression.

### Concept & Theory
* **Greedy Approach:** At each step, select the two minimum frequency subtrees and combine them into a parent node whose frequency is the sum of both children.
* **Lossless Compression:** The exact original string can be reconstructed without any data loss.
* **Prefix Rule:** No code assigned to any character is a prefix of any other character's code, preventing ambiguity during decoding.
* **Frequency-dependent length:** High-frequency characters get the shortest codes, while rare characters get longer codes.

### Algorithm Steps:
1. Count the frequency of each distinct character.
2. Insert each unique character as a leaf node into a min-priority queue sorted by frequency.
3. While the queue contains more than one node:
   - Extract the two nodes with the lowest frequencies: $left$ and $right$.
   - Create a new internal node $z$ with frequency $= left.freq + right.freq$.
   - Assign $left$ as the left child (edge `0`) and $right$ as the right child (edge `1`).
   - Insert $z$ back into the priority queue.
4. The remaining node is the root of the Huffman Tree.
5. Traverse from root to each leaf to assign binary prefix codes (append `0` for left branch, `1` for right branch).

### Code - A2_HuffmanEncoding.java
```java
import java.util.*;

public class A2_HuffmanEncoding {

    public static class HuffmanNode implements Comparable<HuffmanNode> {
        public Character ch;
        public int freq;
        public HuffmanNode left;
        public HuffmanNode right;
        public boolean isLeaf;
        public int creationOrder;

        public HuffmanNode(Character ch, int freq, int creationOrder) {
            this.ch = ch;
            this.freq = freq;
            this.left = null;
            this.right = null;
            this.isLeaf = (ch != null);
            this.creationOrder = creationOrder;
        }

        public HuffmanNode(int freq, HuffmanNode left, HuffmanNode right, int creationOrder) {
            this.ch = null;
            this.freq = freq;
            this.left = left;
            this.right = right;
            this.isLeaf = false;
            this.creationOrder = creationOrder;
        }

        @Override
        public int compareTo(HuffmanNode other) {
            if (this.freq != other.freq) {
                return Integer.compare(this.freq, other.freq);
            }
            if (this.isLeaf != other.isLeaf) {
                return this.isLeaf ? 1 : -1;
            }
            return Integer.compare(this.creationOrder, other.creationOrder);
        }
    }

    public static HuffmanNode buildHuffmanTree(Map<Character, Integer> freqMap) {
        if (freqMap == null || freqMap.isEmpty()) return null;

        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();
        int orderCounter = 0;
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            pq.add(new HuffmanNode(entry.getKey(), entry.getValue(), orderCounter++));
        }

        if (pq.size() == 1) {
            HuffmanNode only = pq.poll();
            return new HuffmanNode(only.freq, only, null, orderCounter++);
        }

        while (pq.size() > 1) {
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
            HuffmanNode parent = new HuffmanNode(left.freq + right.freq, left, right, orderCounter++);
            pq.add(parent);
        }

        return pq.peek();
    }

    public static void generateCodes(HuffmanNode node, String prefix, Map<Character, String> codeMap) {
        if (node == null) return;
        if (node.isLeaf) {
            codeMap.put(node.ch, prefix.isEmpty() ? "0" : prefix);
            return;
        }
        generateCodes(node.left, prefix + "0", codeMap);
        generateCodes(node.right, prefix + "1", codeMap);
    }

    public static String encode(String text, Map<Character, String> codeMap) {
        StringBuilder encoded = new StringBuilder();
        for (char c : text.toCharArray()) {
            encoded.append(codeMap.get(c));
        }
        return encoded.toString();
    }

    public static String decode(String bitString, HuffmanNode root) {
        if (root == null || bitString == null || bitString.isEmpty()) return "";
        if (root.left != null && root.right == null && root.left.isLeaf) {
            return String.valueOf(root.left.ch).repeat(bitString.length());
        }

        StringBuilder decoded = new StringBuilder();
        HuffmanNode curr = root;
        for (int i = 0; i < bitString.length(); i++) {
            curr = (bitString.charAt(i) == '0') ? curr.left : curr.right;
            if (curr != null && curr.isLeaf) {
                decoded.append(curr.ch);
                curr = root;
            }
        }
        return decoded.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("=== Huffman Encoding (Greedy Strategy) ===");
        System.out.println("Choose Input Mode:");
        System.out.println("  1. Enter text string (e.g. BCAADDDCCACACAC)");
        System.out.println("  2. Enter character-frequency table (e.g. a:10, e:15, ...)");
        System.out.print("Enter choice (1 or 2) or paste string directly: ");

        if (!scanner.hasNextLine()) return;
        String line = scanner.nextLine().trim();
        while (line.isEmpty() && scanner.hasNextLine()) {
            line = scanner.nextLine().trim();
        }

        Map<Character, Integer> freqMap = new LinkedHashMap<>();
        String inputString = null;

        if (line.equals("1")) {
            System.out.print("Enter string to encode: ");
            inputString = scanner.nextLine().trim();
            for (char c : inputString.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }
        } else if (line.equals("2")) {
            System.out.print("Enter number of distinct characters: ");
            int n = scanner.nextInt();
            scanner.nextLine();
            System.out.println("Enter each character and frequency (e.g., 'a 10' or 'a:10'):");
            for (int i = 0; i < n; i++) {
                System.out.print("Character " + (i + 1) + ": ");
                String row = scanner.nextLine().trim();
                while (row.isEmpty() && scanner.hasNextLine()) {
                    row = scanner.nextLine().trim();
                }
                String[] parts = row.replace(":", " ").split("\\s+");
                char c = parts[0].charAt(0);
                int f = Integer.parseInt(parts[1]);
                freqMap.put(c, f);
            }
        } else {
            inputString = line;
            for (char c : inputString.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }
        }

        if (freqMap.isEmpty()) return;

        HuffmanNode root = buildHuffmanTree(freqMap);
        Map<Character, String> codeMap = new LinkedHashMap<>();
        generateCodes(root, "", codeMap);

        System.out.println("\n-------------------------------------------------------------");
        System.out.printf("%-12s %-12s %-15s %-12s%n", "Character", "Frequency", "Huffman Code", "Bits (Freq*Len)");
        System.out.println("-------------------------------------------------------------");

        int totalFrequency = 0;
        int totalEncodedBits = 0;
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            char c = entry.getKey();
            int freq = entry.getValue();
            String code = codeMap.get(c);
            int bits = freq * code.length();
            totalFrequency += freq;
            totalEncodedBits += bits;
            System.out.printf("%-12s %-12d %-15s %-12d%n", "'" + c + "'", freq, code, bits);
        }
        System.out.println("-------------------------------------------------------------");

        double avgCodeLength = (double) totalEncodedBits / totalFrequency;
        int uncompressedBits = totalFrequency * 8;

        System.out.println("Total characters in message        : " + totalFrequency);
        System.out.println("Length of encoded message (in bits): " + totalEncodedBits + " bits");
        System.out.printf(Locale.US, "Average code length                : %.3f bits/character%n", avgCodeLength);
        System.out.println("Original uncompressed size (ASCII) : " + uncompressedBits + " bits (" + totalFrequency + " bytes)");
        double savings = (1.0 - ((double) totalEncodedBits / uncompressedBits)) * 100.0;
        System.out.printf(Locale.US, "Storage space saved                : %.2f%%%n", savings);

        if (inputString != null) {
            String encodedString = encode(inputString, codeMap);
            String decodedString = decode(encodedString, root);
            System.out.println("\nEncoded Bitstring:\n" + encodedString);
            System.out.println("\nDecoded String (Verification):\n" + decodedString);
            System.out.println("Lossless reconstruction: " + (inputString.equals(decodedString) ? "PASSED" : "FAILED"));
        }
    }
}
```

### Lab Manual Solved Example
Given frequencies:
`a: 10`, `e: 15`, `i: 12`, `o: 3`, `u: 4`, `s: 13`, `t: 1`

1. **Tree merge trace:**
   - Merge `t(1)` + `o(3)` $\rightarrow$ node `4`
   - Merge node `4` + `u(4)` $\rightarrow$ node `8`
   - Merge node `8` + `a(10)` $\rightarrow$ node `18`
   - Merge `i(12)` + `s(13)` $\rightarrow$ node `25`
   - Merge `e(15)` + node `18` $\rightarrow$ node `33`
   - Merge node `25` + node `33` $\rightarrow$ Root node `58`
2. **Resulting Huffman Codes:**
   - `a = 111`
   - `e = 10`
   - `i = 00`
   - `o = 11001`
   - `u = 1101`
   - `s = 01`
   - `t = 11000`
3. **Metrics:**
   - Total encoded message length: $10(3) + 15(2) + 12(2) + 3(5) + 4(4) + 13(2) + 1(5) = \mathbf{146\text{ bits}}$
   - Average code length: $146 / 58 = \mathbf{2.517\text{ bits/character}}$

### Complexity Analysis
* **Time Complexity:** $O(n \log n)$ where $n$ is the number of unique characters.
  * Building heap: $O(n)$ or $O(n \log n)$.
  * Extract-min is called $2(n - 1)$ times, each taking $O(\log n)$.
  * Overall: $\mathbf{O(n \log n)}$.
* **Space Complexity:** $O(n)$ to store tree nodes and priority queue.

### Assignment Questions & Answers (from Lab Manual)
1. **What is Huffman Encoding?**
   > Huffman Encoding is a greedy, variable-length prefix coding algorithm developed by David Huffman for lossless data compression. It assigns shorter binary codes to more frequent characters and longer codes to less frequent characters.
2. **How many bits may be required for encoding the message ‘mississippi’?**
   > 'mississippi' has length 11 with frequencies: $i: 4, s: 4, p: 2, m: 1$.
   > Huffman codes: $s = 0$, $i = 10$, $m = 110$, $p = 111$.
   > Total bits: $4(1) + 4(2) + 1(3) + 2(3) = 4 + 8 + 3 + 6 = \mathbf{21\text{ bits}}$ (vs 88 bits uncompressed).
3. **Which tree is used in Huffman encoding? Give one example.**
   > An extended full binary tree (strictly binary tree where every internal node has exactly two children) called a **Huffman Tree**. Leaves hold original characters; left and right edges are labeled `0` and `1`.
4. **Why is Huffman coding lossless compression?**
   > Because the complete original data can be reconstructed bit-for-bit during decoding without discarding any information, guaranteed by the unique prefix property of the Huffman tree.

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
