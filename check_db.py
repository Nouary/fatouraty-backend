import sqlite3

conn = sqlite3.connect('fatouraty.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables: {tables}")

# Show columns for factures table if it exists
if any('factures' in t for t in tables):
    cursor.execute("PRAGMA table_info(factures)")
    columns = cursor.fetchall()
    print(f"Factures columns: {columns}")
else:
    print("Factures table doesn't exist")

conn.close()
