import pandas as pd
import sqlite3

# Load the spreadsheets into pandas DataFrames
spreadsheet0 = pd.read_excel('spreadsheet0.xlsx')
spreadsheet1 = pd.read_excel('spreadsheet1.xlsx')
spreadsheet2 = pd.read_excel('spreadsheet2.xlsx')

# Spreadsheet 0 can be directly inserted into the database
def insert_spreadsheet0_to_db(data):
    conn = sqlite3.connect('shipping_data.db')
    cursor = conn.cursor()
    
    # Create the table for spreadsheet0 data (adjust as necessary)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spreadsheet0_data (
        column1 TEXT,
        column2 INTEGER,
        column3 TEXT
    )
    ''')
    
    # Insert data into the table
    for index, row in data.iterrows():
        cursor.execute('''
        INSERT INTO spreadsheet0_data (column1, column2, column3)
        VALUES (?, ?, ?)
        ''', (row['column1'], row['column2'], row['column3']))  # Replace with actual column names
    
    conn.commit()
    conn.close()

# Insert spreadsheet1 and spreadsheet2 data
def insert_spreadsheet1_and_2_to_db(spreadsheet1, spreadsheet2):
    # Merge spreadsheet1 with spreadsheet2 on shipping_id
    merged_data = pd.merge(spreadsheet1, spreadsheet2, on='shipping_id', how='left')

    conn = sqlite3.connect('shipping_data.db')
    cursor = conn.cursor()

    # Create the table for merged data (adjust schema as needed)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shipments (
        shipping_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        origin TEXT,
        destination TEXT
    )
    ''')

    # Insert the merged data into the table
    for index, row in merged_data.iterrows():
        cursor.execute('''
        INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
        VALUES (?, ?, ?, ?, ?)
        ''', (row['shipping_id'], row['product_name'], row['quantity'], row['origin'], row['destination']))

    conn.commit()
    conn.close()

# Insert data from spreadsheet0 into the database
insert_spreadsheet0_to_db(spreadsheet0)

# Insert merged data from spreadsheet1 and spreadsheet2 into the database
insert_spreadsheet1_and_2_to_db(spreadsheet1, spreadsheet2)

print("Data successfully inserted into the database.")
