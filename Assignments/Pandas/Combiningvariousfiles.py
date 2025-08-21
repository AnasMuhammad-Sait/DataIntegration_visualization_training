import pandas as pd

file_path="CustomerSales_2025.xlsx"

sheet_names=pd.ExcelFile(file_path).sheet_names

print(sheet_names)
df_jan=pd.read_excel(file_path,sheet_name=sheet_names[0])
print("jan Data\n")
print(df_jan)
df_feb=pd.read_excel(file_path,sheet_name=sheet_names[1])
print("\n Feb data \n")
print(df_feb)

df_combined=pd.concat([pd.read_excel(file_path,sheet_name=sheet) for sheet in sheet_names])

df_combined.reset_index(drop=True,inplace=True)

df_combined.to_csv("CusomerSales2025Combined.csv")