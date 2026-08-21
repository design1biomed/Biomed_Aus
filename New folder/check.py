import sqlite3
try:
    conn = sqlite3.connect('db.sqlite3')
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables:", [t[0] for t in tables])
    
    # Try different potential table names for EmailConfiguration
    for table in ['main_emailconfiguration', 'main_emailconfig', 'email_configuration', 'emailconfiguration']:
        if table in [t[0] for t in tables]:
            print(f"Found table: {table}")
            data = conn.execute(f"SELECT * FROM {table}").fetchall()
            print("Data:", data)
except Exception as e:
    print("Error:", e)
