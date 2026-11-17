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
