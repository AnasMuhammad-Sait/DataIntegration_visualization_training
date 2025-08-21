# Scenario based data integration and analysis with pandas 

# online store --> sales_csv.csv
# retail stores --> sales_excel.xlsx
# API responses --> df_dict
# Warehouse database --> sales_db.sqlite
# Mobile Sales App --> sales_json.json

import pandas as pd
import sqlite3

df_csv = pd.read_csv("sales_csv.csv")

df_excel=pd.read_excel("sales_excel.xlsx")

df_json=pd.read_json("sales_json.json")

df_dict = pd.DataFrame({
    "order_no": [501, 502],
    "client": ["Ivy", "Jack"],
    "product_name": ["Tablet", "Laptop"],
    "qty_ordered": [2, 1],
    "unit_cost": [650, 1250],
    "date_of_order": pd.to_datetime(["2024-05-02", "2024-05-03"])
})

conn=sqlite3.connect("sales_db.sqlite")
df_sql=pd.read_sql_query("SELECT * FROM Sales",conn)
conn.close()

def standardize(df):
    df.columns = df.columns.str.lower().str.strip()
    df.rename(columns={
        'quantity': 'qty_ordered',
        'quantity_ordered': 'qty_ordered',
        'unitprice': 'unit_cost',
        'price': 'unit_cost',
        'product': 'product_name',
        'orderdate': 'date_of_order'
    }, inplace=True)
    df['date_of_order'] = pd.to_datetime(df['date_of_order'])
    return df

# all the data is standardized and to ensure that there is a connection with the original dataset a source column is added 
df_csv = standardize(df_csv)
df_excel = standardize(df_excel)
df_dict = standardize(df_dict)
df_sql = standardize(df_sql)
df_json = standardize(df_json)

df_csv['Source'] = 'Online Store'
df_excel['Source'] = 'Retail Store'
df_dict['Source'] = 'API'
df_sql['Source'] = 'Warehouse DB'
df_json['Source'] = 'Mobile App'

# combine all the data on to a variable called df_combined
df_combined = pd.concat([df_csv, df_excel, df_dict, df_sql, df_json], ignore_index=True)
print(df_combined)

# Creation of Derived Columns for the better understanding of data 
df_combined['TotalAmount'] = df_combined['qty_ordered'] * df_combined['unit_cost']
df_combined['Month'] = df_combined['date_of_order'].dt.to_period('M')

# Section 1 
# Understanding the data and its Quality 

# 1.
total_records = len(df_combined)
print("Total_Records:",(total_records))

# 2. 
missing = df_combined[['product_name', 'qty_ordered', 'unit_cost']].isnull().sum()
print("Missing values:\n", missing)

# Section 2 
# Transformation and Aggregation

# 3. 
df_combined['TotalAmount'] = df_combined['qty_ordered'] * df_combined['unit_cost']
revenue_by_source = df_combined.groupby('Source')['TotalAmount'].sum().reset_index()
print(revenue_by_source)

# 4.
qty_per_product = df_combined.groupby('product_name')['qty_ordered'].sum().reset_index()
print(qty_per_product)

# 5.
monthly_sales = df_combined.groupby('Month')['TotalAmount'].sum().reset_index()
top_month = monthly_sales.sort_values(by='TotalAmount', ascending=False).head(1)
print("Top month:\n", top_month)

#Section 3 - Business Insights 
# 6.
top_customers = df_combined.groupby('client')['TotalAmount'].sum().reset_index()
top_customers = top_customers.sort_values(by='TotalAmount', ascending=False).head(3)
print(top_customers)

# 7.
product_revenue = df_combined.groupby('product_name').agg(
    total_revenue=('TotalAmount', 'sum'),
    order_count=('order_no', 'count')
).reset_index()

top_product = product_revenue.sort_values(by='total_revenue', ascending=False).head(1)
print(top_product)

# 8.
aov = df_combined['TotalAmount'].mean()
print("Average Order Value (AOV):", round(aov, 2))

# Section 4 - Anomaly Detection 
# 9.
top_unit_prices = df_combined.sort_values(by='unit_cost', ascending=False).head(5)
print(top_unit_prices[['order_no', 'client', 'product_name', 'unit_cost']])

# 10.
mean_price = df_combined['unit_cost'].mean()
std_price = df_combined['unit_cost'].std()

upper_limit = mean_price + 3 * std_price
lower_limit = mean_price - 3 * std_price

outliers = df_combined[(df_combined['unit_cost'] > upper_limit) | (df_combined['unit_cost'] < lower_limit)]
print(outliers[['order_no', 'product_name', 'unit_cost']])
