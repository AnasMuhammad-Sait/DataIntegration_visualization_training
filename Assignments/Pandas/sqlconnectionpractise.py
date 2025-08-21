import pandas as pd
import pyodbc

conn = pyodbc.connect(
    'DRIVER ={ODBC DRIVER 17 for SQL Server};'
    'SERVER = Conect'
)