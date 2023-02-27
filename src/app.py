from pulp import *
from flask import  Flask, jsonify, request
app = Flask(__name__)

prob = LpProblem("Simple Diet Problem",LpMinimize)


import pyodbc

server = 'castingcalc.database.windows.net' # to specify an alternate port
database = 'castingcalc' 
username = 'admCastingCalc' 
password = 'akg234FMQV' 


cnxn_str = ("Driver={SQL Server};"
            "Server="+server+";"
            "Database="+database+";"
            "UID="+username+";"
            "PWD="+password+";")

@app.route("/", methods=["POST"])
def solve():
    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM formulas_simulacion")
    tables = cursor.fetchall()
    #cursor.execute("SELECT WORK_ORDER.TYPE,WORK_ORDER.STATUS, WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID FROM WORK_ORDER")
    costs = {}
    carbono = {}
    si = {}
    mn = {}
    s = {}
    p = {}
    mg = {}
    cu = {}
    cr = {}
    ni = {}
    ti = {}
    v = {}
    mo = {}
    w = {}
    nb = {}
    sn = {}

    materials = []

    #costs = dict(zip(materials,df['Coste']))


    for row in tables:
        materials.append(row.IDmaterial)
        costs[row.IDmaterial] = row.NetPrice
        carbono[row.IDmaterial] = row.C
        si[row.IDmaterial] = row.Si
        mn[row.IDmaterial] = row.Mn
        s[row.IDmaterial]  = row.S
        p[row.IDmaterial]  = row.P
        mg[row.IDmaterial] = row.Mg
        cu[row.IDmaterial] = row.Cu
        cr[row.IDmaterial] = row.Cr
        ni[row.IDmaterial] = row.Ni
        ti[row.IDmaterial] = row.Ti
        v[row.IDmaterial]  = row.V
        mo[row.IDmaterial] = row.Mo
        w[row.IDmaterial]  = row.W
        nb[row.IDmaterial] = row.Nb
        sn[row.IDmaterial] = row.Sn

    print(row.IDmaterial)


    material_vars = LpVariable.dicts("Material", materials, lowBound=0, cat="Integer")


    prob += lpSum([costs[i] * material_vars[i] for i in materials])

    for material in materials:
        if material != 'AST0004' and material != 'VAL0003':
            prob += lpSum([1 * material_vars[material]]) >= 0
            prob += lpSum([1 * material_vars[material]]) <= 100
        else:
            prob += lpSum([1 * material_vars[material]]) >= 15
            prob += lpSum([1 * material_vars[material]]) <= 30

    prob += lpSum([1 * material_vars[i] for i in materials]) == 100

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
        name = str(v.name).split("_")[1]
        if v.varValue>0:
            print(name, "=", v.varValue)
            #print(str(v.name)[9:])
            prueba[name] = v.varValue
            cursor.execute("update formulas_simulacion set optimum = "+str(v.varValue)+" where IDmaterial = '"+name+"';")
        else:
            cursor.execute("update formulas_simulacion set optimum = 0 where IDmaterial = '"+name+"';")
    cursor.commit()
    obj = value(prob.objective) / 100
    print("The total cost is: ${}".format(round(obj,2)))

if __name__ == '__main__':
    app.run(debug=True, port=4000)