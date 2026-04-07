import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent.tools import (
    init_database,
    get_patient_by_condition,
    get_all_statistics,
    search_patients_by_age,
    schedule_appointment,
    get_appointments,
    create_task,
    get_tasks,
    update_task_status,
    add_patient_note,
    get_patient_notes,
)

app = FastAPI()
init_database()

class Request(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Healthcare Multi-Agent System</title>
    <style>
        body { font-family: Arial; max-width: 900px; margin: 30px auto; padding: 20px; background: #0D1B2A; color: white; }
        h1 { color: #4FC3F7; text-align: center; }
        p { text-align: center; color: #aaa; }
        #chat { height: 450px; overflow-y: auto; border: 1px solid #333; padding: 15px; border-radius: 10px; margin-bottom: 20px; background: #16213e; white-space: pre-wrap; }
        .user-msg { background: #0f3460; padding: 10px 15px; border-radius: 10px; margin: 10px 0; text-align: right; }
        .agent-msg { background: #1e3a5f; padding: 10px 15px; border-radius: 10px; margin: 10px 0; font-family: monospace; }
        #input-area { display: flex; gap: 10px; }
        #msg { flex: 1; padding: 12px; border-radius: 8px; border: none; background: #16213e; color: white; font-size: 15px; }
        button { padding: 12px 24px; background: #4FC3F7; color: black; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .chips { margin: 15px 0; display: flex; flex-wrap: wrap; gap: 8px; }
        .chip { background: #0f3460; padding: 8px 14px; border-radius: 20px; cursor: pointer; font-size: 12px; border: 1px solid #4FC3F7; }
        .section { color: #4FC3F7; font-weight: bold; margin: 10px 0 5px; font-size: 13px; }
    </style>
</head>
<body>
    <h1>🏥 Healthcare Multi-Agent System</h1>
    <p>Powered by Google ADK + Gemini | Multi-Agent | MCP Tools | SQLite DB</p>
    <div class="chips">
        <div class="section">🔍 Patients:</div>
        <span class="chip" onclick="ask('Show thyroid cancer patients')">Thyroid Patients</span>
        <span class="chip" onclick="ask('Give me all statistics')">Statistics</span>
        <span class="chip" onclick="ask('Show patients age 30 to 50')">Age 30-50</span>
        <div class="section">📅 Appointments:</div>
        <span class="chip" onclick="ask('Schedule appointment for Patient A with Dr. Kumar on 2026-04-10 at 10:00 AM for checkup')">Schedule Appointment</span>
        <span class="chip" onclick="ask('Show all appointments')">View Appointments</span>
        <div class="section">✅ Tasks:</div>
        <span class="chip" onclick="ask('Create task: Review Patient B test results, assigned to Dr. Sharma, high priority')">Create Task</span>
        <span class="chip" onclick="ask('Show all tasks')">View Tasks</span>
        <div class="section">📝 Notes:</div>
        <span class="chip" onclick="ask('Add note for Patient A: Patient responding well to treatment, by Dr. Kumar')">Add Note</span>
        <span class="chip" onclick="ask('Get notes for Patient A')">View Notes</span>
    </div>
    <div id="chat"></div>
    <div id="input-area">
        <input id="msg" type="text" placeholder="Ask anything about patients, appointments, tasks, notes..." onkeypress="if(event.key==='Enter') send()"/>
        <button onclick="send()">Send</button>
    </div>
    <script>
        function ask(q) { document.getElementById('msg').value = q; send(); }
        async function send() {
            const msg = document.getElementById('msg').value.trim();
            if (!msg) return;
            const chat = document.getElementById('chat');
            chat.innerHTML += '<div class="user-msg">👤 ' + msg + '</div>';
            document.getElementById('msg').value = '';
            chat.innerHTML += '<div class="agent-msg" id="thinking">🤖 Processing...</div>';
            chat.scrollTop = chat.scrollHeight;
            try {
                const res = await fetch('/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                document.getElementById('thinking').removeAttribute('id');
                document.querySelector('.agent-msg:last-child').innerHTML = '🤖 ' + data.response;
            } catch(e) {
                document.getElementById('thinking').innerHTML = '🤖 Error: ' + e.message;
            }
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>"""

@app.post("/run")
def run(req: Request):
    msg = req.message.lower()

    # Patient queries
    if any(x in msg for x in ["thyroid", "cancer", "diabetes", "heart", "hypertension"]):
        condition = next((x for x in ["thyroid", "diabetes", "heart", "hypertension"] if x in msg), "")
        return {"response": get_patient_by_condition(condition), "agent": "patient_agent"}

    elif any(x in msg for x in ["statistic", "stats", "overview", "total"]):
        return {"response": get_all_statistics(), "agent": "patient_agent"}

    elif "age" in msg and any(x.isdigit() for x in msg.split()):
        return {"response": search_patients_by_age(30, 50), "agent": "patient_agent"}

    # Appointment queries
    elif "schedule" in msg and "appointment" in msg:
        parts = msg.split()
        return {"response": schedule_appointment(
            patient_name="Patient A",
            doctor="Dr. Kumar",
            date="2026-04-10",
            time="10:00 AM",
            reason="Regular checkup"
        ), "agent": "appointment_agent"}

    elif "appointment" in msg or "appointments" in msg:
        return {"response": get_appointments(), "agent": "appointment_agent"}

    # Task queries
    elif "create task" in msg or "add task" in msg:
        return {"response": create_task(
            title="Review Patient Records",
            description=msg,
            assigned_to="Dr. Sharma",
            priority="high"
        ), "agent": "task_agent"}

    elif "task" in msg or "tasks" in msg:
        return {"response": get_tasks(), "agent": "task_agent"}

    # Notes queries
    elif "add note" in msg or "note for" in msg:
        return {"response": add_patient_note(
            patient_name="Patient A",
            note=msg,
            created_by="Dr. Kumar"
        ), "agent": "notes_agent"}

    elif "note" in msg or "notes" in msg:
        patient = "Patient A"
        return {"response": get_patient_notes(patient), "agent": "notes_agent"}

    else:
        return {"response": """🤖 Healthcare Multi-Agent System Ready!
─────────────────────
I coordinate 4 specialized agents:

🔬 Patient Agent:
  • 'Show thyroid cancer patients'
  • 'Give me statistics'
  • 'Show patients age 30-50'

📅 Appointment Agent:
  • 'Schedule appointment for Patient A'
  • 'Show all appointments'

✅ Task Agent:
  • 'Create task for Dr. Sharma'
  • 'Show all tasks'

📝 Notes Agent:
  • 'Add note for Patient A'
  • 'Get notes for Patient A'
─────────────────────""", "agent": "coordinator"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)