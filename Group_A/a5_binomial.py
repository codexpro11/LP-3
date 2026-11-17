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
