import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
    )
"""
)

# Insert dummy data
users =[
    (1, "Dhiraj", "dhiraj@example.com", "Jodhpur"),
    (2, "Amit", "amit@example.com", "Delhi"),
    (3, "Sara", "sara@example.com", "London")
]

cursor.executemany("INSERT OR REPLACE INTO users VALUES (?,?,?,?)",users)

conn.commit()
conn.close()

print("Database initialized with dummy data")