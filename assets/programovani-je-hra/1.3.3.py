a = 5
b = 7
c = 3

if a < b:
    if a < c:
        print(a)

        if b < c:
            print(b)
            print(c)
        else:
            print(c)
            print(b)
    else:
        print(c)
        print(a)
        print(b)
else:
    if c < a:
        if c < b:
            print(c)
            print(b)
        else:
            print(b)
            print(c)
        print(a)
    else:
        print(b)
        print(a)
        print(c)

