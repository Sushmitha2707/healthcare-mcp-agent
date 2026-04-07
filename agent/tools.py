import sqlite3
import json
from datetime import datetime

DB_PATH = "data/healthcare.db"

def init_database():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            condition TEXT,
            treatment TEXT,
            doctor TEXT,
            status TEXT
        )
    """)
    
    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor TEXT,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'scheduled'
        )
    """)
    
    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            assigned_to TEXT,
            priority TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    """)
    
    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            note TEXT,
            created_by TEXT,
            created_at TEXT
        )
    """)
    
    # Insert sample patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        patients = [
            (1, "Patient A", 45, "Thyroid Cancer", "Surgery", "Dr. Kumar", "Recovered"),
            (2, "Patient B", 32, "Diabetes Type 2", "Insulin Therapy", "Dr. Sharma", "Ongoing"),
            (3, "Patient C", 58, "Hypertension", "Medication", "Dr. Patel", "Recovered"),
            (4, "Patient D", 27, "Thyroid Cancer", "Radiation", "Dr. Kumar", "Ongoing"),
            (5, "Patient E", 65, "Heart Disease", "Surgery", "Dr. Reddy", "Recovered"),
            (6, "Patient F", 41, "Diabetes Type 2", "Diet Control", "Dr. Sharma", "Recovered"),
            (7, "Patient G", 53, "Hypertension", "Lifestyle Change", "Dr. Patel", "Ongoing"),
            (8, "Patient H", 38, "Thyroid Cancer", "Chemotherapy", "Dr. Kumar", "Ongoing"),
            (9, "Patient I", 72, "Heart Disease", "Medication", "Dr. Reddy", "Recovered"),
            (10, "Patient J", 29, "Diabetes Type 1", "Insulin Pump", "Dr. Sharma", "Ongoing"),
        ]
        cursor.executemany(
            "INSERT INTO patients VALUES (?,?,?,?,?,?,?)", patients
        )
    
    conn.commit()
    conn.close()

# ─── PATIENT TOOLS ───────────────────────────────────────

def get_patient_by_condition(condition: str) -> str:
    """Get patients by medical condition"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM patients WHERE condition LIKE ?",
        (f"%{condition}%",)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return f"No patients found with condition: {condition}"
    result = f"Found {len(rows)} patients with {condition}:\n"
    for r in rows:
        result += f"""
👤 {r[1]} | Age: {r[2]}
🏥 Condition: {r[3]} | 💊 Treatment: {r[4]}
👨‍⚕️ Doctor: {r[5]} | ✅ Status: {r[6]}
─────────────────────"""
    return result

def get_all_statistics() -> str:
    """Get overall healthcare statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(age) FROM patients")
    avg_age = round(cursor.fetchone()[0], 1)
    cursor.execute("SELECT MIN(age), MAX(age) FROM patients")
    min_age, max_age = cursor.fetchone()
    cursor.execute(
        "SELECT condition, COUNT(*) FROM patients GROUP BY condition"
    )
    conditions = cursor.fetchall()
    conn.close()
    result = f"""
📊 Healthcare Database Statistics
─────────────────────
👥 Total Patients: {total}
📅 Age Range: {min_age} - {max_age} years
📊 Average Age: {avg_age} years
─────────────────────
🏥 Conditions:
"""
    for c in conditions:
        result += f"  • {c[0]}: {c[1]} patients\n"
    return result

def search_patients_by_age(min_age: int, max_age: int) -> str:
    """Search patients by age range"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM patients WHERE age BETWEEN ? AND ?",
        (min_age, max_age)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return f"No patients between age {min_age}-{max_age}"
    result = f"Found {len(rows)} patients aged {min_age}-{max_age}:\n"
    for r in rows:
        result += f"👤 {r[1]} | Age: {r[2]} | {r[3]} | Status: {r[6]}\n"
    return result

# ─── APPOINTMENT TOOLS ───────────────────────────────────

def schedule_appointment(
    patient_name: str,
    doctor: str,
    date: str,
    time: str,
    reason: str
) -> str:
    """Schedule a new appointment"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO appointments 
           (patient_name, doctor, date, time, reason) 
           VALUES (?,?,?,?,?)""",
        (patient_name, doctor, date, time, reason)
    )
    conn.commit()
    appt_id = cursor.lastrowid
    conn.close()
    return f"""
✅ Appointment Scheduled!
─────────────────────
🆔 ID: {appt_id}
👤 Patient: {patient_name}
👨‍⚕️ Doctor: {doctor}
📅 Date: {date} at {time}
📝 Reason: {reason}
─────────────────────"""

def get_appointments(doctor: str = None) -> str:
    """Get all appointments or filter by doctor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if doctor:
        cursor.execute(
            "SELECT * FROM appointments WHERE doctor LIKE ?",
            (f"%{doctor}%",)
        )
    else:
        cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No appointments found!"
    result = f"📅 Found {len(rows)} appointments:\n─────────────────────\n"
    for r in rows:
        result += f"""
🆔 {r[0]} | 👤 {r[1]} | 👨‍⚕️ {r[2]}
📅 {r[3]} at {r[4]} | 📝 {r[5]}
Status: {r[6]}
─────────────────────"""
    return result

# ─── TASK TOOLS ──────────────────────────────────────────

def create_task(
    title: str,
    description: str,
    assigned_to: str,
    priority: str = "medium"
) -> str:
    """Create a new task"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """INSERT INTO tasks 
           (title, description, assigned_to, priority, created_at)
           VALUES (?,?,?,?,?)""",
        (title, description, assigned_to, priority, created_at)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return f"""
✅ Task Created!
─────────────────────
🆔 Task ID: {task_id}
📋 Title: {title}
📝 Description: {description}
👤 Assigned To: {assigned_to}
⚡ Priority: {priority}
🕐 Created: {created_at}
─────────────────────"""

def get_tasks(assigned_to: str = None) -> str:
    """Get all tasks or filter by assignee"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if assigned_to:
        cursor.execute(
            "SELECT * FROM tasks WHERE assigned_to LIKE ?",
            (f"%{assigned_to}%",)
        )
    else:
        cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No tasks found!"
    result = f"📋 Found {len(rows)} tasks:\n─────────────────────\n"
    for r in rows:
        result += f"""
🆔 {r[0]} | 📋 {r[1]}
📝 {r[2]}
👤 {r[3]} | ⚡ Priority: {r[4]} | Status: {r[5]}
─────────────────────"""
    return result

def update_task_status(task_id: int, status: str) -> str:
    """Update task status"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, task_id)
    )
    conn.commit()
    conn.close()
    return f"✅ Task {task_id} updated to: {status}"

# ─── NOTES TOOLS ─────────────────────────────────────────

def add_patient_note(
    patient_name: str,
    note: str,
    created_by: str
) -> str:
    """Add a note for a patient"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """INSERT INTO notes 
           (patient_name, note, created_by, created_at)
           VALUES (?,?,?,?)""",
        (patient_name, note, created_by, created_at)
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return f"""
✅ Note Added!
─────────────────────
🆔 Note ID: {note_id}
👤 Patient: {patient_name}
📝 Note: {note}
👨‍⚕️ By: {created_by}
🕐 At: {created_at}
─────────────────────"""

def get_patient_notes(patient_name: str) -> str:
    """Get all notes for a patient"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM notes WHERE patient_name LIKE ?",
        (f"%{patient_name}%",)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return f"No notes found for {patient_name}"
    result = f"📝 Notes for {patient_name}:\n─────────────────────\n"
    for r in rows:
        result += f"""
🆔 {r[0]} | 🕐 {r[4]}
📝 {r[2]}
👨‍⚕️ By: {r[3]}
─────────────────────"""
    return result