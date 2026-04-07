from google.adk.agents import Agent
from agent.tools import (
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

# Sub-Agent 1: Patient Information Agent
patient_agent = Agent(
    model="gemini-2.5-flash",
    name="patient_agent",
    instruction="""You are a Patient Information Specialist.
    You help users find patient records, medical conditions,
    and healthcare statistics.
    Use the available tools to answer patient-related queries.
    Always provide clear, organized responses.""",
    tools=[
        get_patient_by_condition,
        get_all_statistics,
        search_patients_by_age,
    ],
)

# Sub-Agent 2: Appointment Scheduling Agent
appointment_agent = Agent(
    model="gemini-2.5-flash",
    name="appointment_agent",
    instruction="""You are an Appointment Scheduling Specialist.
    You help users schedule, view, and manage doctor appointments.
    When scheduling, always confirm the details before saving.
    Use the available tools to manage appointments.""",
    tools=[
        schedule_appointment,
        get_appointments,
    ],
)

# Sub-Agent 3: Task Management Agent
task_agent = Agent(
    model="gemini-2.5-flash",
    name="task_agent",
    instruction="""You are a Task Management Specialist.
    You help doctors and staff create, view, and update tasks.
    Organize tasks by priority and status.
    Use the available tools to manage tasks.""",
    tools=[
        create_task,
        get_tasks,
        update_task_status,
    ],
)

# Sub-Agent 4: Notes Agent
notes_agent = Agent(
    model="gemini-2.5-flash",
    name="notes_agent",
    instruction="""You are a Medical Notes Specialist.
    You help doctors add and retrieve patient notes.
    Always organize notes clearly with timestamps.
    Use the available tools to manage patient notes.""",
    tools=[
        add_patient_note,
        get_patient_notes,
    ],
)