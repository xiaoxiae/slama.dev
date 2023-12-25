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

def if_leq_zero_instruction():
    return [f"je už hotové?"]

def if_leq_zero(c1, c2):
    l_c1 = get_random_label()
    l_end = get_random_label()

    return (
        if_leq_zero_instruction()
        + jump(l_c1)
        + c2
        + jump(l_end)
        + label(l_c1)
        + c1
        + label(l_end)
    )


def if_leq_one(c1, c2):
    return 


def repeat_until_leq_zero(r, code):
    l_loop = get_random_label()
    l_end = get_random_label()

    return (
        label(l_loop)
        + set_current(r)
        + if_leq_zero_instruction()
        + jump(l_end)
        + code
        + set_current(r)
        + dec()
        + jump(l_loop)
        + label(l_end)
    )

def while_not_leq_zero(r, code):
    l_loop = get_random_label()
    l_end = get_random_label()

    return (
        label(l_loop)
        + set_current(r)
        + if_leq_zero_instruction()
        + jump(l_end)
        + code
        + jump(l_loop)
        + label(l_end)
    )

def zero_out(r):
    return set_(r, 0)

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

    return zero_out(r2) + repeat_until_leq_zero(
        r1,
        set_current(r2) + inc() + set_current(r) + inc(),
    ) + repeat_until_leq_zero(
        r,
        set_current(r1) + inc(),
    )

def move(r1, r2):
    r = get_random_register()

    return zero_out(r2) + repeat_until_leq_zero(
        r1,
        set_current(r2) + inc(),
    )

def subtract(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()

    return (
        zero_out(r3)
        + copy(r1, r_t1)
        + copy(r2, r_t2)
        + repeat_until_leq_zero(
            r_t1,
            set_current(r3) + inc(),
        )
        + repeat_until_leq_zero(
            r_t2,
            set_current(r3) + dec(),
        )
    )

    return copy()

def add(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()

    return (
        zero_out(r3)
        + copy(r1, r_t1)
        + copy(r2, r_t2)
        + repeat_until_leq_zero(
            r_t1,
            set_current(r3) + inc(),
        )
        + repeat_until_leq_zero(
            r_t2,
            set_current(r3) + inc(),
        )
    )

    return copy()

def multiply(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()
    r_t3 = get_random_register()

    return zero_out(r3) + copy(r1, r_t1) + repeat_until_leq_zero(
        r_t1,
        copy(r2, r_t2)
        + repeat_until_leq_zero(
            r_t2,
            set_current(r3) + inc(),
        ),
    )

def divide(r1, r2, r3):
    r_t1 = get_random_register()
    r_tmp = get_random_register()

    return zero_out(r3) + copy(r1, r_t1) + set_current(r_t1) + inc() + while_not_leq_zero(
        r_t1,
        subtract(r_t1, r2, r_tmp) + copy(r_tmp, r_t1) + set_current(r3) + inc(),
    ) + zero_out(r_t1) + zero_out(r_tmp) + set_current(r3) + dec()

def mod(r1, r2, r3):
    r_t1 = get_random_register()
    r_t2 = get_random_register()

    return divide(r1, r2, r_t1) + multiply(r2, r_t1, r_t2) + subtract(r1, r_t2, r3) + zero_out(r_t1) + zero_out(r_t2)


def simulate(contents, debug=False):
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
            if registers[current] <= 0:
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

        if debug:
            print(registers)

        i += 1

    return registers


def run_file(name):
    with open(name, "r") as f:
        contents = f.read().strip().splitlines()

        registers = simulate(contents)

run_file("ss.txt")
quit()


def reverse(r1, r2):
    r1cp = get_random_register()
    tmp1 = get_random_register()
    tmp2 = get_random_register()
    ten = get_random_register()

    return copy(r1, r1cp) + set_(ten, 10) + while_not_leq_zero(
        r1cp,
        mod(r1cp, ten, tmp1) + multiply(r2, ten, tmp2) + add(tmp1, tmp2, r2) + divide(r1cp, ten, tmp1) + move(tmp1, r1cp)
    ) + zero_out(tmp1) + zero_out(tmp2) + zero_out(ten)


def print_register(r):
    r_rev = get_random_register()
    ten = get_random_register()
    n48 = get_random_register()
    tmp1 = get_random_register()
    tmp2 = get_random_register()

    # printing ten prints newline (handy :)
    non_zero_code = reverse(r, r_rev) + while_not_leq_zero(
        r_rev,
        mod(r_rev, ten, tmp1) + add(tmp1, n48, tmp2) + set_current(tmp2) + p() + divide(r_rev, ten, tmp1) + move(tmp1, r_rev)
    ) + zero_out(tmp1) + zero_out(tmp2)

    zero_code = set_current(n48) + p()

    return set_(ten, 10) + set_(n48, 48) + set_current(r) + if_leq_zero(
        zero_code,
        non_zero_code,
    ) + set_current(ten) + p() + zero_out(ten) + zero_out(n48)


def format(code):
    for i, line in enumerate(code):
        if "'" in line:
            code[i] = code[i].replace("'", '<span class="orange">', 1)
            code[i] = code[i].replace("'", '\'</span>', 1)
            code[i] = code[i].replace(">", '>\'', 1)

    return code

def advanced():
    def ex_add():
        return set_("a", 1) + set_("b", 2) + add("a", "b", "c")

    def ex_sub():
        return set_("a", 1) + set_("b", 2) + subtract("a", "b", "c")

    def ex_mul():
        return set_("a", 1) + set_("b", 2) + multiply("a", "b", "c")

    def ex_div():
        return set_("a", 1) + set_("b", 2) + divide("a", "b", "c")

    def ex_preg():
        return set_("a", 123) + print_register("a")

    def ex_fib():
        f1 = get_random_register()
        f2 = get_random_register()
        tmp = get_random_register()

        return set_("a", 10) + set_(f1, 0) + set_(f2, 1) + print_register(f1) + print_register(f2) + repeat_until_leq_zero(
            "a",
            add(f1, f2, tmp) + move(f2, f1) + move(tmp, f2) + print_register(f2)
        )

    def ex_prime():
        a_cp = get_random_register()
        count_down = get_random_register()
        count_up = get_random_register()
        tmp1 = get_random_register()
        tmp2 = get_random_register()

        # from 2 to a...
        return set_("a", 135) + copy("a", count_down) + copy("a", a_cp) \
                + set_current(count_down) + dec() + dec() \
                + set_current(count_up) + inc() + inc() \
                + repeat_until_leq_zero(
            count_down,
            (
                mod(a_cp, count_up, tmp1)
                + set_current(tmp1) \
                + if_leq_zero(
                    divide(a_cp, count_up, tmp2) + move(tmp2, a_cp) + print_register(count_up),
                    set_current(count_up) + inc()
                )
            )
        ) + set_current(a_cp) + dec() + if_leq_zero(
            inc(),
            inc() + print_register(a_cp),
        )

    with open("ss.txt", "w") as f:
        f.write("--ADD--\n")
        for row in format(ex_add()):
            f.write(row + "\n")

        f.write("--SUB--\n")
        for row in format(ex_sub()):
            f.write(row + "\n")

        f.write("--MUL--\n")
        for row in format(ex_mul()):
            f.write(row + "\n")

        f.write("--DIV--\n")
        for row in format(ex_div()):
            f.write(row + "\n")

        f.write("--PREG--\n")
        for row in format(ex_preg()):
            f.write(row + "\n")

        f.write("--FIB--\n")
        for row in format(ex_fib()):
            f.write(row + "\n")

        f.write("--PRIME--\n")
        for row in format(ex_prime()):
            f.write(row + "\n")

advanced()
quit()
