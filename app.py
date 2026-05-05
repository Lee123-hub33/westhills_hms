import psycopg2
import os
from dotenv import load_dotenv

# Load the secrets from .env
load_dotenv()

def fetch_opd_digital_register(): # <--- Name updated to match the call below
    try:
        # Connect using environment variables
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        # Pulling from the new OPD View
        cur.execute("SELECT * FROM opd_digital_register;")
        rows = cur.fetchall()
        
        print("\n--- WESTHILLS HMS: DIGITAL OPD REGISTER ---")
        
        # Indented correctly to be inside the try block
        for row in rows:
            print(f"No: {row[0]} | Date: {row[1]} | Sex: {row[2]} | Age: {row[3]}")
            print(f"Area: {row[4]} | Lab: {row[5]}")
            print(f"Diagnosis: {row[6]} | Treatment: {row[7]}")
            print(f"Balance: KSh {row[10]}")
            print("-" * 40)
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    fetch_opd_digital_register() # <--- This now matches the function name above