a = 10

i = 2
while i <= a:
    while a % i == 0:
        print(i)
        a /= i
    i += 1

