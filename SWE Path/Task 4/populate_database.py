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
    cursor.executemany('''
    INSERT INTO spreadsheet0_data (column1, column2, column3)
    VALUES (?, ?, ?)
    ''', data[['column1', 'column2', 'column3']].values.tolist())  # Replace with actual column names
    
    conn.commit()
    conn.close()

# Insert spreadsheet1 and spreadsheet2 data
def insert_spreadsheet1_and_2_to_db(spreadsheet1, spreadsheet2):
    # Merge spreadsheet1 with spreadsheet2 on shipping_id
    merged_data = pd.merge(spreadsheet1, spreadsheet2, on='shipping_id', how='left')

    # Handle NaN values by replacing them with defaults
    merged_data = merged_data.fillna({
        'product_name': '',  # Default empty string for text fields
        'quantity': 0,       # Default 0 for numeric fields
        'origin': '',        # Default empty string for text fields
        'destination': ''    # Default empty string for text fields
    })

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

    # Insert the merged data into the table using executemany for better performance
    cursor.executemany('''
    INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
    VALUES (?, ?, ?, ?, ?)
    ''', merged_data[['shipping_id', 'product_name', 'quantity', 'origin', 'destination']].values.tolist())

    conn.commit()
    conn.close()

# Insert data from spreadsheet0 into the database
insert_spreadsheet0_to_db(spreadsheet0)

# Insert merged data from spreadsheet1 and spreadsheet2 into the database
insert_spreadsheet1_and_2_to_db(spreadsheet1, spreadsheet2)

print("Data successfully inserted into the database.")