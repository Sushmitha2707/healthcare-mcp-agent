import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from agent.tools import init_database
from agent.sub_agents import (
    patient_agent,
    appointment_agent,
    task_agent,
    notes_agent,
)

load_dotenv()

# Initialize database on startup
init_database()

# Primary Coordinator Agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="healthcare_coordinator",
    instruction="""You are the Healthcare Multi-Agent Coordinator.
    You coordinate multiple specialized sub-agents to help users
    manage healthcare workflows including:

    🏥 Patient Information → Use patient_agent
    📅 Appointments → Use appointment_agent
    ✅ Tasks → Use task_agent
    📝 Notes → Use notes_agent

    Route user requests to the appropriate sub-agent.
    For complex requests involving multiple areas,
    coordinate between agents to provide complete responses.

    Examples:
    - "Show thyroid patients" → patient_agent
    - "Schedule appointment" → appointment_agent
    - "Create task for Dr. Kumar" → task_agent
    - "Add note for Patient A" → notes_agent
    - "Show all appointments and create a task" → both agents

    Always provide clear, helpful, organized responses.""",
    sub_agents=[
        patient_agent,
        appointment_agent,
        task_agent,
        notes_agent,
    ],
)