

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

cnxn = pyodbc.connect(cnxn_str)

cursor = cnxn.cursor()

cursor.execute("SELECT * FROM formulas_simulacion")
tables = cursor.fetchall()
#cursor.execute("SELECT WORK_ORDER.TYPE,WORK_ORDER.STATUS, WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID FROM WORK_ORDER")
data = {}
for row in tables:
    data[row.IDmaterial] = row.C
print(row.IDmaterial)