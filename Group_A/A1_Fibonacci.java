import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class A1_Fibonacci {
    public static List<Integer> fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }

        List<Integer> result = new ArrayList<>();
        int a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            result.add(a);
            int temp = a + b;
            a = b;
            b = temp;
        }

        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Number of terms: ");
        int n = scanner.nextInt();
        List<Integer> terms = fibonacci(n);
        System.out.println("Fibonacci: " + terms);
    }
}
