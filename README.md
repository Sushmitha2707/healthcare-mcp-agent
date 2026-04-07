# 🏥 Healthcare Multi-Agent System

An AI-powered Healthcare Multi-Agent System built using **Google ADK**, **Gemini 2.5 Flash**, **MCP Tools**, and **FastAPI** — developed as part of **Gen AI Academy APAC**.

The system uses a **coordinator agent** that routes requests to 4 specialized sub-agents to manage patients, appointments, tasks, and medical notes.

---

## 🏗️ Architecture


User Request
↓
Healthcare Coordinator Agent (root_agent)
↓
┌────────────────────────────────────────┐
│ 🔬 Patient Agent │ 📅 Appointment │
│ 📝 Notes Agent │ ✅ Task Agent │
└────────────────────────────────────────┘
↓
SQLite Database (4 Tables)


---

## 🚀 Features

- 🤖 **Multi-Agent Architecture** — Coordinator + 4 specialized sub-agents  
- 🗄️ **SQLite Database** — Patients, Appointments, Tasks, Notes tables  
- 🔧 **10 MCP Tools** — Distributed across agents  
- 🌐 **FastAPI Web UI** — Interactive chat interface  
- ☁️ **Cloud Run Deployment** — Publicly accessible  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Google ADK | Agent Development Kit |
| Gemini 2.5 Flash | LLM Model |
| Model Context Protocol (MCP) | Tool integration |
| FastAPI | Web API & UI |
| SQLite | Local database |
| Docker | Containerized deployment |
| Google Cloud Run | Cloud hosting |

---

## 📁 Project Structure


healthcare-mcp-agent/
├── agent/
│ ├── init.py
│ ├── agent.py
│ ├── sub_agents.py
│ └── tools.py
├── data/
│ └── healthcare.db
├── main.py
├── requirements.txt
├── Dockerfile
└── .env


---

## 🧠 Agents & Tools

### 🔬 Patient Agent
| Tool | Description |
|---|---|
| `get_patient_by_condition` | Find patients by condition |
| `get_all_statistics` | Dataset insights |
| `search_patients_by_age` | Filter by age |

### 📅 Appointment Agent
| Tool | Description |
|---|---|
| `schedule_appointment` | Book appointment |
| `get_appointments` | View appointments |

### ✅ Task Agent
| Tool | Description |
|---|---|
| `create_task` | Create task |
| `get_tasks` | View tasks |
| `update_task_status` | Update status |

### 📝 Notes Agent
| Tool | Description |
|---|---|
| `add_patient_note` | Add notes |
| `get_patient_notes` | Retrieve notes |

---

## ☁️ Live Demo & Deployment

### 🚀 Live Application

👉 https://healthcare-mcp-agent-684229547172.us-central1.run.app/

This is a fully deployed and working version of the system.

---

### 🧪 Try These Queries

- Show thyroid cancer patients  
- Give me all statistics  
- Show patients age 30-50  
- Schedule appointment for Patient A  
- Create task for Dr. Sharma  
- Add note for Patient A  

---

## ☁️ Deploy on Google Cloud Run

### 1️⃣ Open Cloud Console  
https://console.cloud.google.com/

### 2️⃣ Activate Cloud Shell

### 3️⃣ Clone Repository
```bash
git clone https://github.com/Sushmitha2707/healthcare-mcp-agent.git
cd healthcare-mcp-agent
4️⃣ Set Project
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region us-central1
5️⃣ Deploy
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --allow-unauthenticated \
  --port 8080
🐳 Run with Docker (Optional)
docker build -t healthcare-mcp-agent .
docker run -p 8080:8080 healthcare-mcp-agent
💬 Example Queries
Query	Agent Used
Show thyroid cancer patients	🔬 Patient Agent
Give me statistics	🔬 Patient Agent
Show patients age 30-50	🔬 Patient Agent
Schedule appointment	📅 Appointment Agent
Create task	✅ Task Agent
Add note	📝 Notes Agent
🎓 Acknowledgements

Built as part of the Gen AI Academy APAC program.

👩‍💻 Author

Sushmitha
GitHub: https://github.com/Sushmitha2707