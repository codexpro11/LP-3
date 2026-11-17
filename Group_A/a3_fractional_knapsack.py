def fractional_knapsack(items, capacity):
    # Each item is (name, weight, value).
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")
    if any(w <= 0 or v < 0 for _, w, v in items):
        raise ValueError("Weights must be positive; values non-negative")

    total = 0.0
    chosen = []
    remaining = float(capacity)
    ordered = sorted(items, key=lambda item: item[2] / item[1],
                     reverse=True)
    for name, weight, value in ordered:
        if remaining <= 0:
            break
        taken_weight = min(weight, remaining)
        fraction = taken_weight / weight
        total += fraction * value
        remaining -= taken_weight
        chosen.append((name, fraction))
    return total, chosen


if __name__ == "__main__":
    n = int(input("Number of items: "))
    items = []
    for i in range(n):
        entry = input(f"Item {i + 1} (Name Weight Value): ").strip().split()
        if len(entry) >= 3:
            name, weight, value = entry[0], float(entry[1]), float(entry[2])
        elif len(entry) == 2:
            name = chr(ord('A') + i) if i < 26 else f"Item{i + 1}"
            weight, value = float(entry[0]), float(entry[1])
        elif len(entry) == 1:
            name = entry[0]
            weight = float(input(f"  Weight for {name}: "))
            value = float(input(f"  Value for {name}: "))
        else:
            name = chr(ord('A') + i) if i < 26 else f"Item{i + 1}"
            weight = float(input(f"  Weight for Item {i + 1}: "))
            value = float(input(f"  Value for Item {i + 1}: "))
        items.append((name, weight, value))

    capacity = float(input("Knapsack capacity: "))
    value, chosen = fractional_knapsack(items, capacity)
    for name, fraction in chosen:
        print(name, "fraction =", round(fraction, 4))
    print("Maximum value:", round(value, 2))
