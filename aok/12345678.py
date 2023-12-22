from random import seed, choice, randint, shuffle

seed(0xdeadbeef)

elements = """
Hydrogen,H,1
Helium,He,2
Lithium,Li,3
Beryllium,Be,4
Boron,B,5
Carbon,C,6
Nitrogen,N,7
Oxygen,O,8
Fluorine,F,9
Neon,Ne,10
Sodium,Na,11
Magnesium,Mg,12
Aluminium,Al,13
Silicon,Si,14
Phosphorus,P,15
Sulfur,S,16
Chlorine,Cl,17
Argon,Ar,18
Potassium,K,19
Calcium,Ca,20
Scandium,Sc,21
Titanium,Ti,22
Vanadium,V,23
Chromium,Cr,24
Manganese,Mn,25
Iron,Fe,26
Cobalt,Co,27
Nickel,Ni,28
Copper,Cu,29
Zinc,Zn,30
Gallium,Ga,31
Germanium,Ge,32
Arsenic,As,33
Selenium,Se,34
Bromine,Br,35
Krypton,Kr,36
Rubidium,Rb,37
Strontium,Sr,38
Yttrium,Y,39
Zirconium,Zr,40
Niobium,Nb,41
Molybdenum,Mo,42
Technetium,Tc,43
Ruthenium,Ru,44
Rhodium,Rh,45
Palladium,Pd,46
Silver,Ag,47
Cadmium,Cd,48
Indium,In,49
Tin,Sn,50
Antimony,Sb,51
Tellurium,Te,52
Iodine,I,53
Xenon,Xe,54
Caesium,Cs,55
Barium,Ba,56
Lanthanum,La,57
Cerium,Ce,58
Praseodymium,Pr,59
Neodymium,Nd,60
Promethium,Pm,61
Samarium,Sm,62
Europium,Eu,63
Gadolinium,Gd,64
Terbium,Tb,65
Dysprosium,Dy,66
Holmium,Ho,67
Erbium,Er,68
Thulium,Tm,69
Ytterbium,Yb,70
Lutetium,Lu,71
Hafnium,Hf,72
Tantalum,Ta,73
Tungsten,W,74
Rhenium,Re,75
Osmium,Os,76
Iridium,Ir,77
Platinum,Pt,78
Gold,Au,79
Mercury,Hg,80
Thallium,Tl,81
Lead,Pb,82
Bismuth,Bi,83
Polonium,Po,84
Astatine,At,85
Radon,Rn,86
Francium,Fr,87
Radium,Ra,88
Actinium,Ac,89
Thorium,Th,90
Protactinium,Pa,91
Uranium,U,92
Neptunium,Np,93
Plutonium,Pu,94
Americium,Am,95
Curium,Cm,96
Berkelium,Bk,97
Californium,Cf,98
Einsteinium,Es,99
Fermium,Fm,100
Mendelevium,Md,101
Nobelium,No,102
Lawrencium,Lr,103
Rutherfordium,Rf,104
Dubnium,Db,105
Seaborgium,Sg,106
Bohrium,Bh,107
Hassium,Hs,108
Meitnerium,Mt,109
Darmstadtium,Ds,110
Roentgenium,Rg,111
Copernicium,Cn,112
Nihonium,Nh,113
Flerovium,Fl,114
Moscovium,Mc,115
Livermorium,Lv,116
Tennessine,Ts,117
Oganesson,Og,118
"""


def gen(name, n, m, o):
    with open(name + ".in", "w") as f:
        h = [line.split(",")[1] for line in elements.strip().splitlines()]

        el = []
        for _ in range(n):
            c = choice(h)
            while c in el or len(c) != 2:
                c = choice(h)

            el.append(c)

        el = sorted(el, key=lambda x: h.index(x))

        for e in el:
            f.write(f"{e}: {randint(o // 10, o - 1)} atoms\n")

        f.write("\n")

        for p in range(m):
            count = randint(1, n)

            t = list(el)
            shuffle(t)

            x = t[:count]

            x = [f"{randint(o // 10, o)}[{i}]" for i in x]

            f.write(" + ".join(x) + " -> " + str(p + 1) + "\n")


def solve_1(name):
    with open(name + ".in", "r") as f:
        counts, lines = f.read().strip().split("\n\n")

        c = {}
        for line in counts.splitlines():
            atom, count, _ = line.split()
            c[atom[:-1]] = int(count)

        total = 0
        for i, line in enumerate(lines.splitlines()):
            line, num = line.split(" -> ")

            works = True
            for req in line.split(" + "):
                e, d = req.split("[")
                d = d[:-1]

                if int(e) > c[d]:
                    works = False

            if works:
                total += int(num)

        return total


def solve_2(name):
    with open(name + ".in", "r") as f:
        counts, lines = f.read().strip().split("\n\n")

        c = {}
        for line in counts.splitlines():
            atom, count, _ = line.split()
            c[atom[:-1]] = int(count)

        c_orig = dict(c)

        for line in lines.splitlines():
            line, _ = line.split(" -> ")

            for req in line.split(" + "):
                e, d = req.split("[")
                d = d[:-1]

                c[d] = max(c[d], int(e))

        total = 0
        for k in c:
            total += c[k] - c_orig[k]

        return total

gen("12345678", n=5, m=5, o=100)
print("1 example:", solve_1("12345678"))
print("2 example:", solve_2("12345678"))

gen("12345678", n=20, m=1000, o=1000)
print("1:", solve_1("12345678"))
print("2:", solve_2("12345678"))
