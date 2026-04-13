import sqlite3

conn = sqlite3.connect("enerfab.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
               id TEXT PRIMARY KEY,
        material TEXT,
        height INTEGER,
        width INTEGER,
        weld_type TEXT,
        cost REAL,
        hours INTEGER
    )
""")
projects = [
    ("PV-2024", "stainless_steel", 10, 4, "standard", 185000, 1200),
    ("PV-3011", "stainless_steel", 11, 4, "standard", 198000, 1350),
    ("PV-4455", "stainless_steel", 9, 5, "corrosion_resistant", 242000, 1500),
    ("RV-108", "carbon_steel", 14, 6, "half_pipe_jacket", 245000, 1800),
    ("RV-512", "carbon_steel", 15, 7, "half_pipe_jacket", 380000, 2100),
    ("RV-610", "carbon_steel", 13, 5, "standard", 210000, 1600),
    ("TK-441", "stainless_steel", 8, 3, "standard", 92000, 600),
    ("TK-780", "carbon_steel", 20, 10, "standard", 315000, 2400),
    ("HX-220", "stainless_steel", 12, 5, "tube_to_tubesheet", 310000, 2100),
    ("HX-335", "stainless_steel", 10, 4, "tube_to_tubesheet", 275000, 1700),
]

cursor.executemany(
    "INSERT OR REPLACE INTO projects VALUES (?, ?, ?, ?, ?, ?, ?)", projects
)

conn.commit()
cursor.execute ("SELECT id, material, cost FROM projects")
rows = cursor.fetchall()

print (f"Database created with {len(rows)} projects:")
for row in rows:
    print (f" {row[0]} - {row[1]} - ${row[2]:,.0f}")
conn.close()