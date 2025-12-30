def fibonacci_iterative(n):
    a = 0
    b = 1

    if n == 0:
        return 0
    if n == 1:
        return 1

    for i in range(0, n - 1):
        c = a + b
        a = b
        b = c

    return b


for i in range(0, 20):
    print(fibonacci_iterative(i))
