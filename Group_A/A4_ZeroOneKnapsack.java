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
