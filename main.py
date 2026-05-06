from fastapi import Header

API_KEY_CREDENTIAL = "westhills_secret_2026" # This is your 'password' for the API

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_CREDENTIAL:
        raise HTTPException(status_code=403, detail="Unauthorized Access")
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from datetime import date

app = FastAPI(title="Westhills HMS - Bondo API")

# --- 1. DATA MODELS (Matches PGAdmin Schema) ---
class PatientCreate(BaseModel):
    name: str
    dob: date       # Format in JSON: "YYYY-MM-DD"
    gender: str     # Use 'M' or 'F' to match your CHECK constraint
    phone: str
    residence: str

# --- 2. DATABASE UTILITY ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="westhills_hms",
        user="postgres",
        password="Lee@2026",
        port="5432"
    )

# --- 3. API ROUTES ---

@app.get("/")
def home():
    return {
        "status": "Online", 
        "hospital": "Westhills HMS", 
        "branch": "Bondo",
        "message": "Clinical Workflow API Ready"
    }

@app.get("/patients")
def get_patients():
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Ordering by created_at so newest patients show first
                cur.execute("SELECT * FROM patients ORDER BY created_at DESC;")
                return cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/patients")
@app.post("/patients")
def register_patient(patient: PatientCreate, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    # Note: patient_id is excluded here because SERIAL generates it automatically
    query = """
    INSERT INTO patients (name, dob, gender, phone, residence) 
    VALUES (%s, %s, %s, %s, %s) RETURNING patient_id;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    patient.name, 
                    patient.dob, 
                    patient.gender, 
                    patient.phone, 
                    patient.residence
                ))
                new_id = cur.fetchone()[0]
                conn.commit()
                return {
                    "status": "Success", 
                    "msg": "Patient registered in Bondo System",
                    "db_id": new_id
                }
    except Exception as e:
        # If gender is not 'M' or 'F', the CHECK constraint will trigger this error
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")