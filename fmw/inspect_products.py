import sqlite3
import json

def inspect_products():
    conn = sqlite3.connect('farmportal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    products = [dict(row) for row in rows]
    print(json.dumps(products, indent=2))
    conn.close()

if __name__ == '__main__':
    inspect_products()
