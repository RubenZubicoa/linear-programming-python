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

prob.solve()

prueba = {}

for v in prob.variables():
    #if v.varValue>0:
        print(v.name, "=", v.varValue)
        print(str(v.name)[9:])
        prueba[v.name] = v.varValue

obj = value(prob.objective)
print("The total cost of this balanced diet is: ${}".format(round(obj,2)))