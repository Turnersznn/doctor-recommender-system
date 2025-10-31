import json
import mysql.connector

# Load JSON file
with open("final_data.json", "r") as f:
    data = json.load(f)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="drs-db"
)
cursor = conn.cursor()

# SQL insert query
insert_query = """
    INSERT INTO doctors (name, specialty, location, experience, availability, rating)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

inserted_rows = 0

for entry in data:
    if isinstance(entry, dict) and "results" in entry:
        for doctor in entry["results"]:
            basic = doctor.get("basic", {})
            taxonomies = doctor.get("taxonomies", [])
            addresses = doctor.get("addresses", [])

            name = f"{basic.get('first_name', '')} {basic.get('middle_name', '')} {basic.get('last_name', '')}".strip()
            specialty = taxonomies[0]["desc"] if taxonomies else "Unknown"
            location = addresses[0]["city"] if addresses else "Unknown"
            experience = 0
            availability = "Available"
            rating = 0

            cursor.execute(insert_query, (name, specialty, location, experience, availability, rating))
            inserted_rows += 1

conn.commit()
cursor.close()
conn.close()

print(f"Inserted {inserted_rows} doctors successfully.")
