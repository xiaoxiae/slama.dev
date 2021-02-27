def fibonacci_recursive(n):
    if n == 0:    # base case
        return 0
    if n == 1:    # base case
        return 1
    else:
        return f(n - 1) + f(n - 2)
    
    
for i in range(0, 20):
    print(fibonacci_recursive(i))
