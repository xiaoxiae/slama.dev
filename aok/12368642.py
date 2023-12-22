from random import seed, choice, randint, shuffle

seed(0xdeadbeef)


l = 3


def gen(name, example=False):
    from string import ascii_lowercase, digits

    if example:
        n = 2
        m = 2
    else:
        n = 8
        m = 3


    def glue(l, used=[None]):
        g = None

        while g in used:
            g = "".join([choice(ascii_lowercase + digits) for _ in range(l)])

        used.append(g)
        return g

    def encode(s):
        s = list(s)

        s[0] = glue(l) + s[0]

        for i in range(len(s) - 1):
            g = glue(l)

            s[i] = s[i] + g
            s[i + 1] = g + s[i + 1]

        s[-1] = s[-1] + glue(l)

        shuffle(s)

        return s

    if example:
        heslo = ["h", "i"]
    else:
        heslo = list("12345678")

    for _ in range(m):
        heslo = "".join(heslo)
        heslo = encode(heslo)

    with open(name + ".in", "w") as f:

        for line in heslo:
            f.write(f"{line}\n")


def solve_1(name):
    with open(name + ".in", "r") as f:
        contents = f.read().strip().splitlines()

        while len(contents) > 1:
            d = {}
            start = set(contents)
            for a in contents:
                for b in contents:
                    if a[-l:] == b[:l]:
                        d[a] = b
                        start -= {b}

            start = list(start)[0]

            o = [start]
            result = ""
            while start in d:
                result += start[len(start) // 2]
                start = d[start]
                o.append(start)
            result += start[len(start) // 2]

            return result[:8]


def solve_2(name):
    with open(name + ".in", "r") as f:
        contents = f.read().strip().splitlines()

        while len(contents) > 1:
            d = {}
            start = set(contents)
            for a in contents:
                for b in contents:
                    if a[-l:] == b[:l]:
                        d[a] = b
                        start -= {b}

            start = list(start)[0]

            o = [start]
            result = ""
            while start in d:
                result += start[len(start) // 2]
                start = d[start]
                o.append(start)
            result += start[len(start) // 2]

            contents = [result[i*7:(i+1)*7]for i in range(len(result) // 7)]

        return result


gen("12368642", example=True)
print("1 example:", solve_1("12368642"))
print("2 example:", solve_2("12368642"))

gen("12368642", example=False)
print("1:", solve_1("12368642"))
print("2:", solve_2("12368642"))
