import pandas
from pulp import *

prob = LpProblem("Simple Diet Problem",LpMinimize)

df = pandas.read_excel("Excel_Solver.xlsx")

materials = list(df['Material'])

costs = dict(zip(materials,df['Coste']))

carbono = dict(zip(materials,df['C']))
si = dict(zip(materials,df['Si']))
mn = dict(zip(materials,df['Mn']))
s = dict(zip(materials,df['S']))
p = dict(zip(materials,df['P']))
mg = dict(zip(materials,df['Mg']))
cu = dict(zip(materials,df['Cu']))
cr = dict(zip(materials,df['Cr']))
ni = dict(zip(materials,df['Ni']))
ti = dict(zip(materials,df['Ti']))
v = dict(zip(materials,df['V']))
mo = dict(zip(materials,df['Mo']))
w = dict(zip(materials,df['W']))
nb = dict(zip(materials,df['Nb']))
sn = dict(zip(materials,df['Sn']))


material_vars = LpVariable.dicts("Material", materials, lowBound=0, cat="Integer")


prob += lpSum([costs[i] * material_vars[i] for i in materials])

# prob += lpSum([1 * material_vars[i] for i in materials]) >= 1, "Min"
# prob += lpSum([1 * material_vars[i] for i in materials]) <= 100, "Max"

for material in materials:
    if material != 'VAL0001' and material != 'VAL0003':
        prob += lpSum([1 * material_vars[material]]) >= 0
        prob += lpSum([1 * material_vars[material]]) <= 100
    else:
        prob += lpSum([1 * material_vars[material]]) >= 15
        prob += lpSum([1 * material_vars[material]]) <= 30

prob += lpSum([1 * material_vars[i] for i in materials]) == 100

# for i in materials:
#     prob += lpSum((carbono[i] * material_vars[i]) / 100) >= 2.5
#     prob += lpSum((carbono[i] * material_vars[i]) / 100) <= 4.2

#     prob += lpSum((si[i] * material_vars[i]) / 100) >= 0.2
#     prob += lpSum((si[i] * material_vars[i]) / 100) <= 1.9

#     prob += lpSum((mn[i] * material_vars[i]) / 100) >= 0.15
#     prob += lpSum((mn[i] * material_vars[i]) / 100) <= 0.2

prob += lpSum([carbono[i] * material_vars[i] for i in materials]) >= 2.5 * 100, "carbonoMin"
prob += lpSum([carbono[i] * material_vars[i] for i in materials]) <= 4.2 * 100, "carbonoMax"
prob += lpSum([si[i] * material_vars[i] for i in materials]) >= 0.2 * 100, "siMin"
prob += lpSum([si[i] * material_vars[i] for i in materials]) <= 1.9 * 100, "siMax"
prob += lpSum([mn[i] * material_vars[i] for i in materials]) >= 0.15 * 100, "mnMin"
prob += lpSum([mn[i] * material_vars[i] for i in materials]) <= 0.2 * 100, "mnMax"
prob += lpSum([s[i] * material_vars[i] for i in materials]) >= 0, "sMin * 100"
prob += lpSum([s[i] * material_vars[i] for i in materials]) <= 0.03 * 100, "sMax"
prob += lpSum([p[i] * material_vars[i] for i in materials]) >= 0, "pMin * 100"
prob += lpSum([p[i] * material_vars[i] for i in materials]) <= 0.03 * 100, "pMax"
prob += lpSum([mg[i] * material_vars[i] for i in materials]) >= 0, "mgMin * 100"
prob += lpSum([mg[i] * material_vars[i] for i in materials]) <= 0.06 * 100, "mgMax"
prob += lpSum([cu[i] * material_vars[i] for i in materials]) >= 0, "cuMin * 100"
prob += lpSum([cu[i] * material_vars[i] for i in materials]) <= 0.01 * 100, "cuMax"
prob += lpSum([cr[i] * material_vars[i] for i in materials]) >= 0, "crMin * 100"
prob += lpSum([cr[i] * material_vars[i] for i in materials]) <= 0.01 * 100, "crMax"
prob += lpSum([ni[i] * material_vars[i] for i in materials]) >= 0, "niMin * 100"
prob += lpSum([ni[i] * material_vars[i] for i in materials]) <= 0.015 * 100, "niMax"
prob += lpSum([ti[i] * material_vars[i] for i in materials]) >= 0, "tiMin * 100"
prob += lpSum([ti[i] * material_vars[i] for i in materials]) <= 0.005 * 100, "tiMax"
prob += lpSum([v[i] * material_vars[i] for i in materials]) >= 0, "vMin * 100"
prob += lpSum([v[i] * material_vars[i] for i in materials]) <= 0.005 * 100, "vMax"
prob += lpSum([mo[i] * material_vars[i] for i in materials]) >= 0, "moMin * 100"
prob += lpSum([mo[i] * material_vars[i] for i in materials]) <= 0.005 * 100, "moMax"
prob += lpSum([w[i] * material_vars[i] for i in materials]) >= 0, "wMin * 100"
prob += lpSum([w[i] * material_vars[i] for i in materials]) <= 0.002 * 100, "wMax"
prob += lpSum([nb[i] * material_vars[i] for i in materials]) >= 0, "nbMin * 100"
prob += lpSum([nb[i] * material_vars[i] for i in materials]) <= 0.002 * 100, "nbMax"
prob += lpSum([sn[i] * material_vars[i] for i in materials]) >= 0, "snMin * 100"
prob += lpSum([sn[i] * material_vars[i] for i in materials]) <= 0.002 * 100, "snMax"

prob.solve()

prueba = {}

for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)
        #print(str(v.name)[9:])
        prueba[v.name] = v.varValue

obj = value(prob.objective) / 100
print("The total cost is: ${}".format(round(obj,2)))