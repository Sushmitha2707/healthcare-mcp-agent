# 🏥 Healthcare Multi-Agent System

An AI-powered Healthcare Multi-Agent System built using Google ADK, Gemini 2.5 Flash, MCP Tools, and FastAPI — developed as part of Gen AI Academy APAC.

The system uses a coordinator agent that routes requests to 4 specialized sub-agents to manage patients, appointments, tasks, and medical notes.

---

## 🌐 Live Demo

👉 https://healthcare-mcp-agent-684229547172.us-central1.run.app/

---

## 🏗️ Architecture

User Request  
↓  
Healthcare Coordinator Agent (root_agent)  
↓  
[ Patient Agent | Appointment Agent | Notes Agent | Task Agent ]  
↓  
SQLite Database (4 Tables)

---

## 🚀 Features

- Multi-Agent Architecture (Coordinator + 4 sub-agents)  
- SQLite Database (Patients, Appointments, Tasks, Notes)  
- MCP Tools integration  
- Multi-step workflows  
- FastAPI Web UI  
- Cloud Run deployment  

---

## 🛠️ Tech Stack

Python 3.10+  
Google ADK  
Gemini 2.5 Flash  
MCP (Model Context Protocol)  
FastAPI  
SQLite  
Docker  
Google Cloud Run  

---

## 📁 Project Structure

healthcare-mcp-agent/  
│  
├── agent/  
│   ├── __init__.py  
│   ├── agent.py  
│   ├── sub_agents.py  
│   └── tools.py  
│  
├── data/  
│   └── healthcare.db  
│  
├── main.py  
├── requirements.txt  
├── Dockerfile  
└── .env  

---

## 🧠 Agents & Tools

Patient Agent  
- get_patient_by_condition  
- get_all_statistics  
- search_patients_by_age  

Appointment Agent  
- schedule_appointment  
- get_appointments  

Task Agent  
- create_task  
- get_tasks  
- update_task_status  

Notes Agent  
- add_patient_note  
- get_patient_notes  

---

## ☁️ Deploy on Google Cloud Run

1️⃣ Clone Repository  
git clone https://github.com/Sushmitha2707/healthcare-mcp-agent.git  
cd healthcare-mcp-agent  

2️⃣ Set Project  
gcloud config set project YOUR_PROJECT_ID  
gcloud config set run/region us-central1  

3️⃣ Deploy  
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --allow-unauthenticated \
  --port 8080  

---

## 🐳 Run with Docker (Optional)

docker build -t healthcare-mcp-agent .  
docker run -p 8080:8080 healthcare-mcp-agent  

---

## 💬 Example Queries

Query                         | Agent Used  
-----------------------------|------------------  
Show thyroid cancer patients | Patient Agent  
Give me statistics           | Patient Agent  
Show patients age 30-50      | Patient Agent  
Schedule appointment         | Appointment Agent  
Create task                  | Task Agent  
Add note                     | Notes Agent  

---

## 🎯 Problem Statement Alignment

- Multi-agent coordination ✔  
- Database integration ✔  
- MCP tools usage ✔  
- Multi-step workflows ✔  
- API-based deployment ✔  

---

## 🎓 Acknowledgements

Built as part of the Gen AI Academy APAC program.

---

## 👩‍💻 Author

Sushmitha  
GitHub: https://github.com/Sushmitha2707