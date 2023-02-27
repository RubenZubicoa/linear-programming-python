

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