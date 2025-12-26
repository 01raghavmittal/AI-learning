def complex_pattern1(n: int = 5):
    space = 0

    # upper half
    for i in range(n):
        for j in range(1, n - i + 1):
            print('*', end="")
        for j in range(0, space):
            print(' ', end="")
        for j in range(1, n - i + 1):
            print('*', end="")
        print()
        space += 2  # increase space after each row

    # lower half
    space = 2 * n - 2
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print('*', end="")
        for j in range(1, space + 1):
            print(' ', end="")
        for j in range(1, i + 1):
            print('*', end="")
        print()
        space -= 2  # decrease space after each row

complex_pattern1()
