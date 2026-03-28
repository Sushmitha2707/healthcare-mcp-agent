import pandas as pd
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("healthcare-server")

# Load dataset
df = pd.read_csv("data/healthcare.csv")

@mcp.tool()
def get_patient_info(condition: str) -> str:
    """Get patient information by medical condition"""
    results = df[df['condition'].str.contains(
        condition, case=False, na=False)]
    if results.empty:
        return f"No patients found with condition: {condition}"
    return results.head(5).to_string()

@mcp.tool()
def get_statistics() -> str:
    """Get overall statistics of the healthcare dataset"""
    stats = f"""
    Total Patients: {len(df)}
    Conditions: {df['condition'].nunique()} unique
    Age Range: {df['age'].min()} - {df['age'].max()}
    Average Age: {df['age'].mean():.1f}
    """
    return stats

@mcp.tool()
def search_by_age(min_age: int, max_age: int) -> str:
    """Search patients by age range"""
    results = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
    if results.empty:
        return f"No patients found between ages {min_age} and {max_age}"
    return results.head(5).to_string()

if __name__ == "__main__":
    mcp.run()