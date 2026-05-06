import psycopg2
from psycopg2.extras import RealDictCursor
import os

# --- 1. CONNECTION LOGIC ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="westhills_hms",
        user="postgres",
        password="Lee@2026",
        port="5432"
    )

# --- 2. STAFF MANAGEMENT ---
def add_new_staff(first_name, last_name, role, phone):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO staff (first_name, last_name, role, phone_number)
        VALUES (%s, %s, %s, %s);
        """
        cur.execute(sql, (first_name, last_name, role, phone))
        conn.commit()
        print(f"Successfully added {role}: {first_name} {last_name}")
    except Exception as e:
        print(f"Database Error while adding staff: {e}")
    finally:
        cur.close()
        conn.close()

# --- 3. PATIENT UPDATES WITH AUDIT LOGGING ---
def update_patient_residence(patient_id, new_residence, staff_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Fetch OLD value for the audit log
        cur.execute("SELECT residence FROM patients WHERE patient_id = %s", (patient_id,))
        old_data = cur.fetchone()
        old_residence = old_data['residence'] if old_data else "Unknown"

        # 2. Perform the UPDATE
        cur.execute(
            "UPDATE patients SET residence = %s WHERE patient_id = %s",
            (new_residence, patient_id)
        )

        # 3. Create the AUDIT LOG entry
        audit_sql = """
        INSERT INTO audit_logs (table_name, record_id, action_type, old_value, new_value, changed_by)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(audit_sql, ('patients', patient_id, 'UPDATE', old_residence, new_residence, staff_id))

        # 4. Commit BOTH as one atomic transaction
        conn.commit()
        print(f"Update successful. Logged change by Staff ID: {staff_id}")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# --- 4. REPORTING FUNCTIONS ---
def view_audit_history():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT a.*, s.first_name, s.role 
            FROM audit_logs a 
            JOIN staff s ON a.changed_by = s.staff_id
            ORDER BY changed_at DESC;
        """)
        logs = cur.fetchall()
        print("\n" + "="*20 + " SYSTEM AUDIT LOGS " + "="*20)
        for log in logs:
            print(f"[{log['changed_at'].strftime('%Y-%m-%d %H:%M')}] {log['first_name']} ({log['role']})")
            print(f"Action: {log['action_type']} on {log['table_name']} #{log['record_id']}")
            print(f"Change: '{log['old_value']}' -> '{log['new_value']}'")
            print("-" * 59)
    except Exception as e:
        print(f"Error fetching logs: {e}")
    finally:
        cur.close()
        conn.close()

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
            # Using your actual column names from the view
            print(f"Vitals:  Temp: {row.get('temp_celsius', 'N/A')}°C | BP: {row.get('blood_pressure', 'N/A')}")
            print(f"Lab:     {row.get('lab_summary', 'N/A')}")
            print(f"Clinical: Diagnosis: {row.get('diagnosis_icd10', 'N/A')}")
            print(f"Plan:    {row.get('treatment_plan', 'N/A')}")
            print("-" * 67)
            print(f"Billing: Total: {row['total_amount']} | Paid: {row['amount_paid']} | Balance: KSh {row['balance']}")
            print(f"{'='*67}\n")
    except Exception as e:
        print(f"Error reading register: {e}")
    finally:
        cur.close()
        conn.close()

# --- 5. EXECUTION BLOCK ---
if __name__ == "__main__":
    # Example: Update patient #1 to 'Bondo' and log it as Staff #1
    # update_patient_residence(1, "Bondo", 1)
    
    # Show the Register
    print_digital_register()
    
    # Show the History
    view_audit_history()