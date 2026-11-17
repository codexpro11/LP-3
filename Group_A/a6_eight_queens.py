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
