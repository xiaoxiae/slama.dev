from random import seed, choice, randint, sample
from string import ascii_lowercase

seed(0xDEADBEEF)


from names import names


def get_random_register():
    return "".join([choice(ascii_lowercase) for _ in range(12)])

def get_random_label():
    return "".join([choice(ascii_lowercase) for _ in range(12)])

def set_current(register):
    return [f"jmenuji se '{register}'"]

def set_value(value):
    return [f"prosím o drink číslo '{value}'"]

def set_(register, value):
    return set_current(register) + set_value(value)

def label(l):
    return [f"včera jsem slyšela o '{l}'"]

def jump(l):
    return [f"to mi připomnělo '{l}'"]

def inc():
    return ["s mlékem"]

def dec():
    return ["bez mléka"]

def comment(c):
    return [f"# {c}"]

def skip():
    return [f""]

def p():
    return ["nápoj je připravený!"]

def if_zero():
    return [f"je už hotové?"]

def repeat_until_zero(r, code):
    l_loop = get_random_label()
    l_end = get_random_label()

    return (
        set_current(r)
        + label(l_loop)
        + if_zero()
        + jump(l_end)
        + code
        + set_current(r)
        + dec()
        + jump(l_loop)
        + label(l_end)
    )

def zero_out(r):
    # could be done easier but we're limit testing
    return repeat_until_zero(r, [])

def p_line(s: str):
    r = get_random_register()

    code = []
    for c in s:
        code += set_(r, ord(c))
        code += p()
    code += zero_out(r)

    return code

def copy(r1, r2):
    r = get_random_register()

    return repeat_until_zero(
        r1,
        set_current(r2) + inc() + set_current(r) + inc(),
    ) + repeat_until_zero(
        r,
        set_current(r1) + inc(),
    )

def subtract(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()

    return (
        copy(r1, r_t1)
        + copy(r2, r_t2)
        + repeat_until_zero(
            r_t1,
            set_current(r3) + inc(),
        )
        + repeat_until_zero(
            r_t2,
            set_current(r3) + dec(),
        )
    )

    return copy()

def add(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()

    return (
        copy(r1, r_t1)
        + copy(r2, r_t2)
        + repeat_until_zero(
            r_t1,
            set_current(r3) + inc(),
        )
        + repeat_until_zero(
            r_t2,
            set_current(r3) + inc(),
        )
    )

    return copy()

def multiply(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()
    r_t3 = get_random_register()

    return copy(r1, r_t1) + repeat_until_zero(
        r_t1,
        copy(r2, r_t2)
        + repeat_until_zero(
            r_t2,
            set_current(r3) + inc(),
        ),
    )


def gen(name):
    with open(name + ".txt", "w") as f:

        test_part = []

        n = 100
        o = 150
        registers = [get_random_register() for _ in range(n)]
        register_values = [randint(0, o) for _ in range(n)]

        for i, r in enumerate(registers):
            test_part += set_(r, register_values[i])

        m = 100
        results = {}
        output_registers = [get_random_register() for _ in range(m)]

        messages = {
            10: "START KALIBRACE\n",
            20: "Varim kafe...\n",
            30: "Zahrivam ponozky...\n",
            50: "Pripravuji mleko...\n",
            75: "Kombinuji...\n",
            99: "HOTOVO!\n",
        }

        for i in range(m):
            a, b = sample(registers, k=2)
            op = choice(["*", "+", "-"])

            a_val = register_values[registers.index(a)]
            b_val = register_values[registers.index(b)]

            results[output_registers[i]] = (
                (a_val + b_val) if op == "+"
                else (a_val - b_val) if op == "-"
                else (a_val * b_val)
            )

            if i in messages:
                test_part += p_line(messages[i])

            if op == "+":
                test_part += add(a, b, output_registers[i])
            elif op == "-":
                test_part += subtract(a, b, output_registers[i])
            else:
                test_part += multiply(a, b, output_registers[i])

        print("Calibration sum:", sum([v for v in results.values()]))

        for i, r in enumerate(registers):
            test_part += zero_out(r)

        message = r"""
   .-.                                                   \ /     
  ( (      Stastne a vesele! <3      |                  - * -    
   '-`                              -+-                  / \     
            \            o          _|_          \               
            ))          }^{        /___\         ))              
          .-#-----.     /|\     .---'-'---.    .-#-----.         
     ___ /_________\   //|\\   /___________\  /_________\        
    /___\ |[] _ []|    //|\\    | A /^\ A |    |[] _ []| _.O,_   
....|"#"|.|  |*|  |...///|\\\...|   |"|   |....|  |*|  |..(^)...."""

        l1 = get_random_label()
        l2 = get_random_label()
        l_end = get_random_label()

        real_part = []

        def prime_factors(n):
            i = 2
            factors = []
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
                    factors.append(i)
            if n > 1:
                factors.append(n)
            return factors


        for j, c in enumerate(message):
            val = ord(c)
            offset = randint(10, 1000)

            new_val = val + offset

            factors = prime_factors(new_val)

            registers = [get_random_register() for _ in factors]

            for i, r in enumerate(registers):
                real_part += set_(r, factors[i])

            r1 = get_random_register()
            tmp = get_random_register()

            real_part += set_(tmp, 1)

            for r in registers:
                real_part += multiply(tmp, r, r1)
                real_part += zero_out(tmp)
                real_part += copy(r1, tmp)
                real_part += zero_out(r1)

            r2 = get_random_register()
            real_part += set_(r2, offset)

            real_part += subtract(r1, r2, tmp)
            real_part += set_current(tmp)
            real_part += p()

        code = set_(get_random_register(), 0) \
                + if_zero() \
                + jump(l2) \
                + jump(l1) \
                + label(l2) \
                + test_part \
                + jump(l_end) \
                + label(l1) \
                + real_part \
                + label(l_end)

        for line in code:
            f.write(line + "\n")


def simulate(contents):
    from collections import defaultdict

    current = None
    registers = defaultdict(int)
    labels = {}

    for i, line in enumerate(contents):
        if line.startswith("včera"):
            labels[line.split("'")[1]] = i

    i = 0
    while i < len(contents):
        line = contents[i]

        if "#" in line:
            line = line.split("#")[0]

        line = line.strip()

        if line.startswith("jmenuji se"):
            current = line.split("'")[1]
        elif line.startswith("#"):
            pass
        elif len(line.strip()) == 0:
            pass
        elif line.startswith("prosím"):
            assert current is not None
            registers[current] = int(line.split("'")[1])
        elif line == "s mlékem":
            registers[current] += 1
        elif line == "bez mléka":
            registers[current] -= 1
        elif line.startswith("včera"):
            pass  # set in a loop before
        elif line.startswith("to mi připomnělo"):
            i = labels[line.split("'")[1]]
        elif line.startswith("je už hotové?"):
            if registers[current] == 0:
                i += 0
            else:
                i += 1
        elif line.startswith("nápoj je připravený!"):
            assert current is not None
            assert 0 <= registers[current] < 128
            print(chr(registers[current]), end="", flush=True)
        else:
            print("Unknown command", line)
            quit()

        i += 1

    return registers


def ex():
    code = set_("a", 1) \
            + set_("b", 2) \
            + skip() \
            + inc() \
            + inc() \
            + skip() \
            + set_current("a") \
            + dec() \
            + dec()

    for row in code:
        print(row)
    print("----------------")
    registers = simulate(code)
    print(registers)
    print("----------------")

    code = skip() \
            + label("loop") \
            + skip() \
            + comment("poběží donekonečna...") \
            + skip() \
            + jump("loop")

    for row in code:
        print(row)
    print("----------------")

    code = set_("repeat", 10) \
            + skip() \
            + label("loop") \
            + set_current("repeat") \
            + if_zero() \
            + jump("end") \
            + skip() \
            + comment("opakuje se desetkrát...") \
            + skip() \
            + set_current("repeat") \
            + dec() \
            + jump("loop") \
            + label("end")

    for row in code:
        print(row)
    print("----------------")
    registers = simulate(code)
    print(registers)
    print("----------------")

    code = set_current("tmp") + skip()

    for c in "Ahoj!":
        code += set_value(ord(c)) + p() + skip()

    for row in code:
        print(row)
    print("----------------")
    registers = simulate(code)
    print(registers)
    print("----------------")

    comments = """
jmenuji se 'a'
prosím o drink číslo '1'  # {a: 1}
jmenuji se 'b'
prosím o drink číslo '2'  # {a: 1, b: 2}

s mlékem            # {a: 1, b: 3}
s mlékem            # {a: 1, b: 4}

jmenuji se 'a'
bez mléka           # {a: 0, b: 4}
bez mléka           # {a: -1, b: 4}
    """

    registers = simulate(comments.splitlines())

    print("----------------")

    code = set_("a", 13) \
            + set_("b", 23) \
            + add("a", "b", "c")

    for row in code:
        print(row)
    print("----------------")
    registers = simulate(code)
    print(registers)
    total = 0
    for r in registers:
        total += registers[r]
    print()
    print(total)
    print("----------------")

    code = set_("a", 31) \
            + set_("b", 15) \
            + multiply("a", "b", "c")

    for row in code:
        print(row)
    print("----------------")
    registers = simulate(code)
    print(registers)
    total = 0
    for r in registers:
        total += registers[r]
    print()
    print(total)
    print("----------------")


def solve_1(name):
    with open(name + ".txt", "r") as f:
        contents = f.read().strip().splitlines()

        registers = simulate(contents)

        total = 0
        for k, v in sorted(registers.items()):
            total += v

        return total


def solve_2(name):
    with open(name + ".txt", "r") as f:
        contents = f.read().strip().splitlines()

        contents[1] = contents[1].replace("0", "1")

        _ = simulate(contents)


gen("things-customers-said-this-year")

print()
print("1:", solve_1("things-customers-said-this-year"))
print()
solve_2("things-customers-said-this-year")
print()

ex()
