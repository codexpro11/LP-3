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
