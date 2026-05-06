import psycopg2
from psycopg2.extras import RealDictCursor
import os

# 1. Define the connection function first
def get_db_connection():
    # Replace these with your actual .env or local credentials
    return psycopg2.connect(
        host="localhost",
        database="westhills_hms", # Ensure this matches your DB name
        user="postgres",
        password="Lee@2026",   # Replace with your actual password
        port="5432"
    )

# 2. Define the printing function
def print_digital_register():
    try:
        conn = get_db_connection()
        # RealDictCursor allows using row['column_name']
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM opd_digital_register;")
        rows = cur.fetchall()

        if not rows:
            print("\n--- No records found in the OPD Register ---\n")
            return

        for row in rows:
            print(f"\n{'='*15} WESTHILLS HMS: DIGITAL OPD REGISTER {'='*15}")
            print(f"ID: {row['visit_id']:<5} | Date: {row['visit_date']}")
            print(f"Patient: {row['gender']} ({row['age']} yrs) | Residence: {row['residence']}")
            print("-" * 67)
            print(f"Vitals:  Temp: {row['temperature']}°C | BP: {row['blood_pressure']}")
            print(f"Lab:     {row['lab_summary']}")
            print(f"Clinical: Diagnosis: {row['diagnosis']}")
            print(f"Plan:    {row['treatment_plan']}")
            print("-" * 67)
            print(f"Billing: Total: {row['total_amount']} | Paid: {row['amount_paid']} | Balance: KSh {row['balance']}")
            print(f"{'='*67}\n")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

# 3. Actually run the code
if __name__ == "__main__":
    print_digital_register()