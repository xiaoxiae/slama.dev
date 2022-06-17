from pulp import *

data = [
        { 'nosnost': 165,
          'hmotnosti': [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
          'ceny': [92, 57, 49, 68, 60, 43, 67, 84, 87, 72] },
        { 'nosnost': 26,
          'hmotnosti': [12, 7, 11, 8, 9],
          'ceny': [24, 13, 23, 15, 16] },
        { 'nosnost': 6404180,
          'hmotnosti': [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684],
          'ceny': [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261] },
        ]

for dataset in data:
    size = len(dataset['hmotnosti'])

    # vytvoření modelu
    model = LpProblem(name="problem-batohu", sense=LpMaximize)

    # proměnné -- zda do batohu vložíme i-tou věc
    variables = [LpVariable(name=f"x{i}", cat='Binary') for i in range(size)]

    # omezení -- nesmíme do batohu vložit více než nosnost
    model += lpSum([dataset['hmotnosti'][i] * variables[i] for i in range(size)]) <= dataset['nosnost']

    # funkce k maximalizaci -- cena věcí v batohu
    model += lpSum([dataset['ceny'][i] * variables[i] for i in range(size)])

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))

    print("cena batohu:", model.objective.value())
    print("vezmeme:", *[int(variables[i].value()) for i in range(size)])
    print()
