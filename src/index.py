import pandas
from pulp import *

prob = LpProblem("Simple Diet Problem",LpMinimize)

df = pandas.read_excel("Excel_Solver.xlsx")

materials = list(df['Material'])

costs = dict(zip(materials,df['Coste']))

carbono = dict(zip(materials,df['C']))



material_vars = LpVariable.dicts("Material", materials, lowBound=0, cat="continuous")


prob += lpSum([costs[i] * material_vars[i] for i in materials])

prob += lpSum([carbono[i] * material_vars[i] for i in materials]) >= 2.5, "carbonoMin"
prob += lpSum([carbono[i] * material_vars[i] for i in materials]) <= 4.2, "carbonoMax"


prob.solve()

for v in prob.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)
