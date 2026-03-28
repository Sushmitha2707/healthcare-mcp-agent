import os
import pandas as pd
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

# Load dataset directly
df = pd.read_csv("data/healthcare.csv")

def get_patient_info(condition: str) -> str:
    """Get patients by medical condition"""
    results = df[df['condition'].str.contains(
        condition, case=False, na=False)]
    if results.empty:
        return f"No patients found with: {condition}"
    return results.to_string()

def get_statistics() -> str:
    """Get overall dataset statistics"""
    return f"""
    Total Patients: {len(df)}
    Unique Conditions: {df['condition'].nunique()}
    Age Range: {df['age'].min()} - {df['age'].max()}
    Average Age: {df['age'].mean():.1f}
    """

def search_by_age(min_age: int, max_age: int) -> str:
    """Search patients by age range"""
    results = df[
        (df['age'] >= min_age) & 
        (df['age'] <= max_age)
    ]
    if results.empty:
        return f"No patients between {min_age}-{max_age}"
    return results.to_string()

root_agent = Agent(
    model="gemini-2.5-flash",
    name="healthcare_assistant",
    instruction="""You are a helpful healthcare data assistant.
    Use the available tools to answer questions about patient data.
    Always provide clear, helpful responses.""",
    tools=[get_patient_info, get_statistics, search_by_age],
)