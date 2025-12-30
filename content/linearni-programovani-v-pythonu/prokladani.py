from pulp import *

# pole bodů, kterými prokládáme
point_lists = [
    [(0, 0), (1, 1)],
    [(3, 2), (-1, 4)],
    [(3, 4), (1, 4), (5, 2), (1, 1.5), (4.5, 3)],
]

for points in point_lists:
    # vytvoření modelu
    model = LpProblem(name="prokladani-primkou", sense=LpMinimize)

    # proměnné -- koeficienty a, b a vzdálenosti od přímky
    a = LpVariable(name="a")
    b = LpVariable(name="b")
    distances = [LpVariable(name=f"d_{i}") for i in range(len(points))]

    # omezení -- vzdálenosti v absolutní hodnotě
    for i, d_i in enumerate(distances):
        model += -d_i <= (a * points[i][0] + b) - points[i][1]
        model += (a * points[i][0] + b) - points[i][1] <= d_i

    # funkce k minimalizaci -- vzdálenosti od přímky
    model += lpSum(distances)

    # řešení (ignorujeme debug zprávy)
    status = model.solve(PULP_CBC_CMD(msg=False))
    print("rovnice přímky: ", f"{a.value()}x + {b.value()}")
