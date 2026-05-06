from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Westhills HMS - Bondo API")

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="westhills_hms",
        user="postgres",
        password="Lee@2026",
        port="5432"
    )

@app.get("/")
def home():
    return {"status": "Online", "hospital": "Westhills HMS", "location": "Bondo"}

@app.get("/patients")
def get_patients():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM patients;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
from pydantic import BaseModel

# 1. Define what a Patient looks like (for the API)
class PatientCreate(BaseModel):
   first_name: str
   last_name: str
   gender: str
   age: int
   residence: str
# 2. Add the Registration Route
@app.post("/patients")
def register_patient(patient: PatientCreate):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Use first_name and last_name from your PatientCreate class
        query = """
        INSERT INTO patients (patient_id, first_name, last_name, gender, age, residence) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING patient_id;
        """
        
        cur.execute(query, (
            patient.patient_id,  # This is your WH-2026-XXXX format
            patient.first_name,  # Corrected from patient.name
            patient.last_name,   # Corrected from patient.name
            patient.gender, 
            patient.age, 
            patient.residence
        ))
        
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"status": "Success", "patient_id": new_id}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()