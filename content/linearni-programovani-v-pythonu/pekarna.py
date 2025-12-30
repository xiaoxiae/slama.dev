from pulp import *

# vytvoření modelu
model = LpProblem(name="problem-pekarny", sense=LpMaximize)

# proměnné -- kolik pečiva upečeme
xc = LpVariable(name="chleby", lowBound=0, cat="Integer")
xh = LpVariable(name="housky", lowBound=0, cat="Integer")
xb = LpVariable(name="bagety", lowBound=0, cat="Integer")
xk = LpVariable(name="koblihy", lowBound=0, cat="Integer")

# omezení -- nesmíme na pečení spotřebovat více surovin než máme
model += 500 * xc + 150 * xh + 230 * xb + 100 * xk <= 5000
model += 10 * xc + 2 * xh + 7 * xb + 1 * xk <= 125
model += 50 * xc + 10 * xh + 15 * xb <= 500

# funkce k maximalizaci -- zisk z pečení
model += 20 * xc + 2 * xh + 10 * xb + 7 * xk

# řešení (ignorujeme debug zprávy)
status = model.solve(PULP_CBC_CMD(msg=False))
print(int(xc.value()), int(xh.value()), int(xb.value()), int(xk.value()))
