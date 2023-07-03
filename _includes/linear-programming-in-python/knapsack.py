from pulp import *


# three datasets (small/medium/large)
# each contains weights / prices / knapsack carry weight
data = [
    [
        "Small",
        [12, 7, 11, 8, 9],
        [24, 13, 23, 15, 16],
        26,
    ],
    [
        "Medium",
        [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
        [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
        165,
    ],
    [
        "Large",
        [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684],
        [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261],
        6404180,
    ],
]

for name, weights, prices, carry_weight in data:
    n = len(weights)

    model = LpProblem(sense=LpMaximize)

    # variables - binary based on if we take the item or not
    variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]

    # inequalities - don't exceed the carry weight
    model += lpDot(weights, variables) <= carry_weight

    # objective function - price of the items we take
    model += lpDot(prices, variables)

    status = model.solve(PULP_CBC_CMD(msg=False))

    print(name + "\n" + "-" * len(name))
    print("price:", model.objective.value())
    print("take:", *[variables[i].value() for i in range(n)])
    print()
