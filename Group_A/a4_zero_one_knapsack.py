def knapsack(weights, values, capacity):
    if len(weights) != len(values):
        raise ValueError("Lengths must match")
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("Capacity must be a non-negative integer")
    if any(not isinstance(w, int) or w <= 0 for w in weights):
        raise ValueError("Weights must be positive integers")

    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, value = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(
                    dp[i][c], value + dp[i - 1][c - w]
                )

    selected = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(i - 1)
            c -= weights[i - 1]
    selected.reverse()
    return dp[n][capacity], selected


if __name__ == "__main__":
    n = int(input("Number of items: "))
    weights = []
    values = []
    for i in range(n):
        entry = input(f"Item {i + 1} (Weight Value): ").strip().split()
        if len(entry) >= 2:
            w, v = int(entry[0]), int(entry[1])
        elif len(entry) == 1:
            w = int(entry[0])
            v = int(input(f"  Value for Item {i + 1}: "))
        else:
            w = int(input(f"  Weight for Item {i + 1}: "))
            v = int(input(f"  Value for Item {i + 1}: "))
        weights.append(w)
        values.append(v)

    capacity = int(input("Knapsack capacity: "))
    best, selected = knapsack(weights, values, capacity)
    print("Maximum value:", best)
    print("Selected item numbers:", [i + 1 for i in selected])
