import pandas
from pulp import *

def addConstraint(problem, amount, component, min, max, componentKey):
    problem += lpSum([(amount * component[i]) * material_vars[i] for i in materials]) >= min, componentKey + "Min"
    problem += lpSum([(amount * component[i]) * material_vars[i] for i in materials]) <= max, componentKey + "Max"

prob = LpProblem("Cantidad de materiales",LpMinimize)
prob2 = LpProblem("Simple Diet Problem",LpMinimize)

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

components = ['c', 'si', 'mn', 's', 'p', 'mg', 'cu', 'cr', 'ni', 'ti', 'v', 'mo', 'w', 'nb', 'sn']


material_vars = LpVariable.dicts("Material", materials, lowBound=0, cat="Integer")


prob += lpSum([costs[i] * material_vars[i] for i in materials])

for material in materials:
    if material != 'VAL0001' and material != 'VAL0003':
        prob += lpSum([1 * material_vars[material]]) >= 0, material + 'Min'
        prob += lpSum([1 * material_vars[material]]) <= 100, material + 'Max'
    else:
        prob += lpSum([1 * material_vars[material]]) >= 15, material + 'Min'
        prob += lpSum([1 * material_vars[material]]) <= 30, material + 'Max'

prob += lpSum([1 * material_vars[i] for i in materials]) == 100, 'Total'

prob.solve()

prueba = {}

for variable in prob.variables():
    #if v.varValue>0:
        print(variable.name, "=", variable.varValue)
        name = str(variable.name)[9:]
        # prueba[name] = v.varValue
        costs[name] = costs[name] * variable.varValue
        carbono[name] = carbono[name] * variable.varValue
        si[name] = si[name] * variable.varValue
        mn[name] = mn[name] * variable.varValue
        s[name] = s[name] * variable.varValue
        p[name] = p[name] * variable.varValue
        mg[name] = mg[name] * variable.varValue
        cu[name] = cu[name] * variable.varValue
        cr[name] = cr[name] * variable.varValue
        ni[name] = ni[name] * variable.varValue
        ti[name] = ti[name] * variable.varValue
        v[name] = v[name] * variable.varValue
        mo[name] = mo[name] * variable.varValue
        w[name] =  w[name] * variable.varValue
        nb[name] =  nb[name] * variable.varValue
        sn[name] =  sn[name] * variable.varValue

material_vars2 = LpVariable.dicts("Component", components, lowBound=0, cat="Continuos")

prob2 += lpSum([costs[i] * material_vars2[i] for i in materials])

prob2 += lpSum([carbono[i] * material_vars2[i] for i in materials]) >= 2.5, "carbonoMin"
prob2 += lpSum([carbono[i] * material_vars2[i] for i in materials]) <= 4.2, "carbonoMax"

prob2 += lpSum([si[i] * material_vars2[i] for i in materials]) >= 0.2, "siMin"
prob2 += lpSum([si[i] * material_vars2[i] for i in materials]) <= 1.9, "siMax"

prob2 += lpSum([mn[i] * material_vars2[i] for i in materials]) >= 0.15, "mnMin"
prob2 += lpSum([mn[i] * material_vars2[i] for i in materials]) <= 0.2, "mnMax"

prob2 += lpSum([s[i] * material_vars2[i] for i in materials]) >= 0, "sMin"
prob2 += lpSum([s[i] * material_vars2[i] for i in materials]) <= 0.03, "sMax"

prob2 += lpSum([p[i] * material_vars2[i] for i in materials]) >= 0, "pMin"
prob2 += lpSum([p[i] * material_vars2[i] for i in materials]) <= 0.03, "pMax"

prob2 += lpSum([mg[i] * material_vars2[i] for i in materials]) >= 0, "mgMin"
prob2 += lpSum([mg[i] * material_vars2[i] for i in materials]) <= 0.06, "mgMax"

prob2 += lpSum([cu[i] * material_vars2[i] for i in materials]) >= 0, "cuMin"
prob2 += lpSum([cu[i] * material_vars2[i] for i in materials]) <= 0.01, "cuMax"

prob2 += lpSum([cr[i] * material_vars2[i] for i in materials]) >= 0, "crMin"
prob2 += lpSum([cr[i] * material_vars2[i] for i in materials]) <= 0.01, "crMax"

prob2 += lpSum([ni[i] * material_vars2[i] for i in materials]) >= 0, "niMin"
prob2 += lpSum([ni[i] * material_vars2[i] for i in materials]) <= 0.015, "niMax"

prob2 += lpSum([ti[i] * material_vars2[i] for i in materials]) >= 0, "tiMin"
prob2 += lpSum([ti[i] * material_vars2[i] for i in materials]) <= 0.005, "tiMax"

prob2 += lpSum([v[i] * material_vars2[i] for i in materials]) >= 0, "vMin"
prob2 += lpSum([v[i] * material_vars2[i] for i in materials]) <= 0.005, "vMax"

prob2 += lpSum([mo[i] * material_vars2[i] for i in materials]) >= 0, "moMin"
prob2 += lpSum([mo[i] * material_vars2[i] for i in materials]) <= 0.005, "moMax"

prob2 += lpSum([w[i] * material_vars2[i] for i in materials]) >= 0, "wMin"
prob2 += lpSum([w[i] * material_vars2[i] for i in materials]) <= 0.002, "wMax"

prob2 += lpSum([nb[i] * material_vars2[i] for i in materials]) >= 0, "nbMin"
prob2 += lpSum([nb[i] * material_vars2[i] for i in materials]) <= 0.002, "nbMax"

prob2 += lpSum([sn[i] * material_vars2[i] for i in materials]) >= 0, "snMin"
prob2 += lpSum([sn[i] * material_vars2[i] for i in materials]) <= 0.002, "snMax"

prob2.solve()

for v in prob2.variables():
    if v.varValue>-1:
        print(v.name, "=", v.varValue)

obj = value(prob2.objective)
print("The total cost of this balanced diet is: ${}".format(round(obj,2)))