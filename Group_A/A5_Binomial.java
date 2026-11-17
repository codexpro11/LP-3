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
