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
