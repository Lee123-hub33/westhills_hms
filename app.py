import psycopg2
from psycopg2.extras import RealDictCursor
import os

# 1. Connection logic
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="westhills_hms",
        user="postgres",
        password="Lee@2026",
        port="5432"
    )

# 2. WRITE Function (Secure against SQL Injection)
def add_new_staff(first_name, last_name, role, phone):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO staff (first_name, last_name, role, phone_number)
        VALUES (%s, %s, %s, %s);
        """
        staff_data = (first_name, last_name, role, phone)

        cur.execute(sql, staff_data)
        conn.commit()
        
        print(f"Successfully added {role}: {first_name} {last_name}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Error while adding staff: {e}")

# 3. READ Function
def print_digital_register():
    try:
        conn = get_db_connection()
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
            print(f"Vitals:  Temp: {row['temp_celsius']}°C | BP: {row['blood_pressure']}")
            print(f"Lab:     {row['lab_summary']}")
            print(f"Clinical: Diagnosis: {row['diagnosis_icd10']}")
            print(f"Plan:    {row['treatment_plan']}")
            print("-" * 67)
            print(f"Billing: Total: {row['total_amount']} | Paid: {row['amount_paid']} | Balance: KSh {row['balance']}")
            print(f"{'='*67}\n")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error reading register: {e}")

# 4. EXECUTION Block
if __name__ == "__main__":
    # To add a staff member, uncomment the line below:
    # add_new_staff("Sarah", "Anyango", "Nurse", "0712345678")
    
    # Run the register report
    print_digital_register()