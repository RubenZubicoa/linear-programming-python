from pulp import *
from flask import  Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pyodbc

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

server = 'castingcalc.database.windows.net' # to specify an alternate port
database = 'optimacasting' 
username = 'admCastingCalc' 
password = 'akg234FMQV' 


cnxn_str = ("Driver={SQL Server};"
            "Server="+server+";"
            "Database="+database+";"
            "UID="+username+";"
            "PWD="+password+";")

@app.route("/<idFormula>/<casting>", methods=["GET"])
def solve(idFormula, casting):
    prob = LpProblem("Minimize costs of production",LpMinimize)
    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM formulas_simulacion where Idformula = '" + idFormula +"' and Casting = '"+ casting +"'")
    tables = cursor.fetchall()
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
    zzMax = {}
    zzMin = {}

    materials = []


    for row in tables:
        if row.IDmaterial != "zzMax" and row.IDmaterial != "zzMin":
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
        else:
            if row.IDmaterial == "zzMax":
                zzMax = row
            else:
                zzMin = row



    material_vars = LpVariable.dicts("Material", materials, lowBound=0, cat="Integer")


    prob += lpSum([costs[i] * material_vars[i] for i in materials])

    for row in tables:
        if row.IDmaterial != 'zzMax' and row.IDmaterial != 'zzMin':
            prob += lpSum([1 * material_vars[row.IDmaterial]]) >= row.Minimum
            prob += lpSum([1 * material_vars[row.IDmaterial]]) <= row.Maximum

    prob += lpSum([1 * material_vars[i] for i in materials]) == 100

    prob += lpSum([carbono[i] * material_vars[i] for i in materials]) >= zzMin.C * 100, "carbonoMin"
    prob += lpSum([carbono[i] * material_vars[i] for i in materials]) <= zzMax.C * 100, "carbonoMax"
    prob += lpSum([si[i] * material_vars[i] for i in materials]) >= zzMin.Si * 100, "siMin"
    prob += lpSum([si[i] * material_vars[i] for i in materials]) <= zzMax.Si * 100, "siMax"
    prob += lpSum([mn[i] * material_vars[i] for i in materials]) >= zzMin.Mn * 100, "mnMin"
    prob += lpSum([mn[i] * material_vars[i] for i in materials]) <= zzMax.Mn * 100, "mnMax"
    prob += lpSum([s[i] * material_vars[i] for i in materials]) >= zzMin.S * 100, "sMin"
    prob += lpSum([s[i] * material_vars[i] for i in materials]) <= zzMax.S * 100, "sMax"
    prob += lpSum([p[i] * material_vars[i] for i in materials]) >= zzMin.P * 100, "pMin"
    prob += lpSum([p[i] * material_vars[i] for i in materials]) <= zzMax.P * 100, "pMax"
    prob += lpSum([mg[i] * material_vars[i] for i in materials]) >= zzMin.Mg * 100, "mgMin"
    prob += lpSum([mg[i] * material_vars[i] for i in materials]) <= zzMax.Mg * 100, "mgMax"
    prob += lpSum([cu[i] * material_vars[i] for i in materials]) >= zzMin.Cu * 100, "cuMin"
    prob += lpSum([cu[i] * material_vars[i] for i in materials]) <= zzMax.Cu * 100, "cuMax"
    prob += lpSum([cr[i] * material_vars[i] for i in materials]) >= zzMin.Cr * 100, "crMin"
    prob += lpSum([cr[i] * material_vars[i] for i in materials]) <= zzMax.Cr * 100, "crMax"
    prob += lpSum([ni[i] * material_vars[i] for i in materials]) >= zzMin.Ni * 100, "niMin"
    prob += lpSum([ni[i] * material_vars[i] for i in materials]) <= zzMax.Ni * 100, "niMax"
    prob += lpSum([ti[i] * material_vars[i] for i in materials]) >= zzMin.Ti * 100, "tiMin"
    prob += lpSum([ti[i] * material_vars[i] for i in materials]) <= zzMax.Ti * 100, "tiMax"
    prob += lpSum([v[i] * material_vars[i] for i in materials]) >= zzMin.V * 100, "vMin"
    prob += lpSum([v[i] * material_vars[i] for i in materials]) <= zzMax.V * 100, "vMax"
    prob += lpSum([mo[i] * material_vars[i] for i in materials]) >= zzMin.Mo * 100, "moMin"
    prob += lpSum([mo[i] * material_vars[i] for i in materials]) <= zzMax.Mo * 100, "moMax"
    prob += lpSum([w[i] * material_vars[i] for i in materials]) >= zzMin.W * 100, "wMin"
    prob += lpSum([w[i] * material_vars[i] for i in materials]) <= zzMax.W * 100, "wMax"
    prob += lpSum([nb[i] * material_vars[i] for i in materials]) >= zzMin.Nb * 100, "nbMin"
    prob += lpSum([nb[i] * material_vars[i] for i in materials]) <= zzMax.Nb * 100, "nbMax"
    prob += lpSum([sn[i] * material_vars[i] for i in materials]) >= zzMin.Sn * 100, "snMin"
    prob += lpSum([sn[i] * material_vars[i] for i in materials]) <= zzMax.Sn * 100, "snMax"

    prob.solve()


    for v in prob.variables():
        name = str(v.name).split("_")[1]
        if v.varValue>0:
            print(name, "=", v.varValue)
            #print(str(v.name)[9:])
            cursor.execute("update formulas_simulacion set optimum = "+str(v.varValue)+" where IDmaterial = '"+name+"' and Idformula = '" + idFormula +"' and Casting = '"+ casting +"';")
        else:
            cursor.execute("update formulas_simulacion set optimum = 0 where IDmaterial = '"+name+"' and Idformula = '" + idFormula +"' and Casting = '"+ casting +"';")
    cursor.commit()
    obj = value(prob.objective) / 100
    print("The total cost is: ${}".format(round(obj,2)))
    return jsonify({"Message":"OK"})

if __name__ == '__main__':
    app.run(debug=True, port=3000)