def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    # Counter bookkeeping itself is not part of the count.
    steps = 1             # n < 0 comparison
    a, b = 0, 1
    result = []
    i = 0
    steps += 4            # a, b, result, i assignments

    while i < n:
        steps += 1        # successful loop comparison
        result.append(a)
        steps += 1        # append
        a, b = b, a + b
        steps += 3        # addition, two assignments
        i = i + 1
        steps += 2        # addition and assignment

    steps += 1            # final failed comparison
    steps += 1            # return
    return result, steps


if __name__ == "__main__":
    n = int(input("Number of terms: "))
    terms, steps = fibonacci(n)
    print("Fibonacci:", terms)
    print("Counted steps:", steps)
    print("Formula 7n + 7:", 7 * n + 7)
