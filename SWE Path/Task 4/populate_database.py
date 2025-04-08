
import pandas as pd # type: ignore
import sqlite3

# Load spreadsheets into DataFrames
spreadsheet0 = pd.read_excel('spreadsheet0.xlsx')
spreadsheet1 = pd.read_excel('spreadsheet1.xlsx')
spreadsheet2 = pd.read_excel('spreadsheet2.xlsx')

# Merge spreadsheet1 with spreadsheet2 based on shipping_id
merged_data = pd.merge(spreadsheet1, spreadsheet2, on='shipping_id', how='left')

# Process the data to extract the necessary columns
final_data = merged_data[['shipping_id', 'product_name', 'quantity', 'origin', 'destination']]

# Connect to the SQLite database
conn = sqlite3.connect('shipping_data.db')
cursor = conn.cursor()

# Example of creating a table (adjust schema as needed)
cursor.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    shipping_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    origin TEXT,
    destination TEXT
)
''')

# Insert the data into the table
for index, row in final_data.iterrows():
    cursor.execute('''
    INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['shipping_id'], row['product_name'], row['quantity'], row['origin'], row['destination']))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data successfully inserted into the database.")
