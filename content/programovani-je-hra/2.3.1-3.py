pole = [1, 2, 5, -1, 3]

maximum = pole[0]
i = 1
while i < len(pole):
    maximum = min(maximum, pole[i])
    i += 1

print(maximum)
