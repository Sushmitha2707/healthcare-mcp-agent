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
│  🔬 Patient Agent  │ 📅 Appointment   │
│  📝 Notes Agent    │ ✅ Task Agent    │
└────────────────────────────────────────┘
↓
SQLite Database (4 Tables)

---

## 🚀 Features

- 🤖 **Multi-Agent Architecture** — Coordinator + 4 specialized sub-agents
- 🗄️ **SQLite Database** — Patients, Appointments, Tasks, Notes tables
- 🔧 **10 MCP Tools** — Distributed across agents
- 🌐 **FastAPI Web UI** — Interactive chat interface
- ☁️ **Cloud Run Ready** — Deployable on Google Cloud Run

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
│   ├── init.py
│   ├── agent.py          # Root coordinator agent
│   ├── sub_agents.py     # 4 specialized sub-agents
│   └── tools.py          # 10 MCP tool functions
├── data/
│   └── healthcare.db     # SQLite database (auto-created)
├── main.py               # FastAPI app + Web UI
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
└── .env                  # Environment variables

---

## 🧠 Agents & Tools

### 🔬 Patient Agent
| Tool | Description |
|---|---|
| `get_patient_by_condition` | Find patients by medical condition |
| `get_all_statistics` | Overall healthcare statistics |
| `search_patients_by_age` | Filter patients by age range |

### 📅 Appointment Agent
| Tool | Description |
|---|---|
| `schedule_appointment` | Book a new appointment |
| `get_appointments` | View all / filter by doctor |

### ✅ Task Agent
| Tool | Description |
|---|---|
| `create_task` | Create a new task |
| `get_tasks` | View all / filter by assignee |
| `update_task_status` | Update task status |

### 📝 Notes Agent
| Tool | Description |
|---|---|
| `add_patient_note` | Add a note for a patient |
| `get_patient_notes` | Retrieve notes for a patient |

---

## ☁️ Setup & Deployment (Google Cloud Run)
1️⃣ Open Google Cloud Shell

Go to:
👉 https://console.cloud.google.com/

Click Activate Cloud Shell

2️⃣ Clone the Repository
git clone https://github.com/Sushmitha2707/healthcare-mcp-agent.git
cd healthcare-mcp-agent
3️⃣ Set Project & Region
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region us-central1
4️⃣ Enable Required Services
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
5️⃣ Deploy to Cloud Run
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --allow-unauthenticated \
  --port 8080
6️⃣ Access Your Application

After deployment, you will get a URL like:

https://healthcare-mcp-agent-xxxxxx.run.app

👉 Open it in browser to use your app 🎉

7️⃣ (Optional) Update Environment Variables

If needed, deploy with environment variables:

gcloud run deploy healthcare-mcp-agent \
  --source . \
  --set-env-vars GOOGLE_API_KEY=your_api_key \
  --allow-unauthenticated \
  --port 8080
✅ Done

👉 This version is:

Clean ✅
Hackathon-ready ✅
Matches Cloud Run deployment ✅

If you want next:
👉 I can optimize your README to look premium (top 5% submissions)
👉 Or review your final GitHub before submission

Just tell 👍

give me to update in code for README file

Here’s your final ready-to-paste README section (only the updated part) 👇
Just replace your current “Setup & Installation” section with this:

## ☁️ Setup & Deployment (Google Cloud Run)

### 1️⃣ Open Google Cloud Console
Go to: https://console.cloud.google.com/  
Click **Activate Cloud Shell**

---

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/Sushmitha2707/healthcare-mcp-agent.git
cd healthcare-mcp-agent
3️⃣ Set Project & Region
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region us-central1
4️⃣ Enable Required Services
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
5️⃣ Deploy to Cloud Run
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --allow-unauthenticated \
  --port 8080
6️⃣ Access the Application

After deployment, you will get a URL like:

https://healthcare-mcp-agent-xxxxxx.run.app

Open it in your browser to use the application.

7️⃣ (Optional) Add Environment Variables
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --set-env-vars GOOGLE_API_KEY=your_api_key \
  --allow-unauthenticated \
  --port 8080
---

## 🐳 Run with Docker
```bash
docker build -t healthcare-mcp-agent .
docker run -p 8080:8080 healthcare-mcp-agent
```

---

## ☁️ Deploy to Google Cloud Run
```bash
gcloud run deploy healthcare-mcp-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

---

## 💬 Example Queries

| Query | Agent Used |
|---|---|
| "Show thyroid cancer patients" | 🔬 Patient Agent |
| "Give me all statistics" | 🔬 Patient Agent |
| "Show patients age 30-50" | 🔬 Patient Agent |
| "Schedule appointment for Patient A" | 📅 Appointment Agent |
| "Show all appointments" | 📅 Appointment Agent |
| "Create task for Dr. Sharma" | ✅ Task Agent |
| "Show all tasks" | ✅ Task Agent |
| "Add note for Patient A" | 📝 Notes Agent |
| "Get notes for Patient A" | 📝 Notes Agent |

---

## 🎓 Acknowledgements

Built as part of the **Gen AI Academy APAC** program.

---

## 👩‍💻 Author

**Sushmitha** — [GitHub](https://github.com/Sushmitha2707)
