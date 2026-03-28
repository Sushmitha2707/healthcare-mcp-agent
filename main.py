# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class Request(BaseModel):
#     message: str

# @app.get("/")
# def home():
#     return {"status": "Healthcare MCP Agent running"}

# @app.post("/run")
# def run(req: Request):
#     return {
#         "response": f"Processed healthcare query: {req.message}"
#     }
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

try:
    df = pd.read_csv("data/healthcare.csv")
except:
    df = None

class Request(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Healthcare MCP Agent</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #1a1a2e; color: white; }
            h1 { color: #4fc3f7; text-align: center; }
            p { text-align: center; color: #aaa; }
            #chat { height: 450px; overflow-y: auto; border: 1px solid #333; padding: 15px; border-radius: 10px; margin-bottom: 20px; background: #16213e; white-space: pre-wrap; }
            .user-msg { background: #0f3460; padding: 10px 15px; border-radius: 10px; margin: 10px 0; text-align: right; }
            .agent-msg { background: #1e3a5f; padding: 10px 15px; border-radius: 10px; margin: 10px 0; font-family: monospace; line-height: 1.6; }
            #input-area { display: flex; gap: 10px; }
            #msg { flex: 1; padding: 12px; border-radius: 8px; border: none; background: #16213e; color: white; font-size: 15px; }
            button { padding: 12px 24px; background: #4fc3f7; color: black; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 15px; }
            button:hover { background: #81d4fa; }
            .chips { margin: 15px 0; display: flex; flex-wrap: wrap; gap: 8px; }
            .chip { background: #0f3460; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 13px; border: 1px solid #4fc3f7; }
            .chip:hover { background: #1a4a8a; }
        </style>
    </head>
    <body>
        <h1>🏥 Healthcare MCP Agent</h1>
        <p>Powered by Google ADK + Gemini | Gen AI Academy APAC</p>
        <div class="chips">
            <span class="chip" onclick="ask('Show thyroid cancer patients')">🔬 Thyroid Cancer</span>
            <span class="chip" onclick="ask('Give me dataset statistics')">📊 Statistics</span>
            <span class="chip" onclick="ask('Show patients age 30 to 50')">👥 Age 30-50</span>
            <span class="chip" onclick="ask('Show all conditions')">🏥 All Conditions</span>
            <span class="chip" onclick="ask('Show diabetes patients')">💊 Diabetes</span>
            <span class="chip" onclick="ask('Show heart disease patients')">❤️ Heart Disease</span>
        </div>
        <div id="chat"></div>
        <div id="input-area">
            <input id="msg" type="text" placeholder="Ask about healthcare data..." onkeypress="if(event.key==='Enter') send()"/>
            <button onclick="send()">Send</button>
        </div>
        <script>
            function ask(q) {
                document.getElementById('msg').value = q;
                send();
            }
            async function send() {
                const msg = document.getElementById('msg').value.trim();
                if (!msg) return;
                const chat = document.getElementById('chat');
                chat.innerHTML += '<div class="user-msg">👤 ' + msg + '</div>';
                document.getElementById('msg').value = '';
                chat.innerHTML += '<div class="agent-msg" id="thinking">🤖 Thinking...</div>';
                chat.scrollTop = chat.scrollHeight;
                try {
                    const res = await fetch('/run', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: msg})
                    });
                    const data = await res.json();
                    const thinking = document.getElementById('thinking');
                    thinking.removeAttribute('id');
                    thinking.innerHTML = '🤖 ' + data.response;
                } catch(e) {
                    document.getElementById('thinking').innerHTML = '🤖 Error: ' + e.message;
                }
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

@app.post("/run")
def run(req: Request):
    msg = req.message.lower()
    if df is None:
        return {"response": "⚠️ Dataset not loaded!"}

    if "thyroid" in msg or "cancer" in msg:
        results = df[df['condition'].str.contains('Thyroid', case=False)]
        formatted = f"Found {len(results)} Thyroid Cancer patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 Patient: {row['name']} (Age: {row['age']})
🏥 Condition: {row['condition']}
💊 Treatment: {row['treatment']}
👨‍⚕️ Doctor: {row['doctor']}
📅 Admitted: {row['admission_date']}
📅 Discharged: {row['discharge_date']}
✅ Status: {row['status']}
─────────────────────"""
        return {"response": formatted}

    elif "statistic" in msg or "stats" in msg or "overview" in msg:
        return {"response": f"""
📊 Healthcare Dataset Overview
─────────────────────
👥 Total Patients: {len(df)}
🏥 Unique Conditions: {int(df['condition'].nunique())}
📅 Age Range: {df['age'].min()} - {df['age'].max()} years
📊 Average Age: {round(df['age'].mean(), 1)} years
─────────────────────
📋 Conditions Breakdown:
""" + "\n".join([f"  • {c}: {len(df[df['condition']==c])} patients"
                  for c in df['condition'].unique()])}

    elif "age" in msg or "30" in msg or "50" in msg:
        results = df[(df['age'] >= 30) & (df['age'] <= 50)]
        formatted = f"Found {len(results)} patients between age 30-50:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
🏥 {row['condition']} | 💊 {row['treatment']}
✅ Status: {row['status']}
─────────────────────"""
        return {"response": formatted}

    elif "condition" in msg or "all" in msg:
        formatted = "🏥 Available Conditions:\n─────────────────────\n"
        for i, c in enumerate(df['condition'].unique(), 1):
            count = len(df[df['condition'] == c])
            formatted += f"{i}. {c} ({count} patients)\n"
        return {"response": formatted}

    elif "diabetes" in msg:
        results = df[df['condition'].str.contains('Diabetes', case=False)]
        formatted = f"Found {len(results)} Diabetes patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
💊 Treatment: {row['treatment']}
👨‍⚕️ Doctor: {row['doctor']}
✅ Status: {row['status']}
─────────────────────"""
        return {"response": formatted}

    elif "heart" in msg:
        results = df[df['condition'].str.contains('Heart', case=False)]
        formatted = f"Found {len(results)} Heart Disease patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
💊 Treatment: {row['treatment']}
👨‍⚕️ Doctor: {row['doctor']}
✅ Status: {row['status']}
─────────────────────"""
        return {"response": formatted}

    elif "hypertension" in msg or "blood pressure" in msg:
        results = df[df['condition'].str.contains('Hypertension', case=False)]
        formatted = f"Found {len(results)} Hypertension patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
💊 Treatment: {row['treatment']}
👨‍⚕️ Doctor: {row['doctor']}
✅ Status: {row['status']}
─────────────────────"""
        return {"response": formatted}

    elif "recover" in msg or "recovered" in msg:
        results = df[df['status'].str.contains('Recovered', case=False)]
        formatted = f"Found {len(results)} Recovered patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
🏥 {row['condition']}
✅ Status: Recovered
─────────────────────"""
        return {"response": formatted}

    elif "ongoing" in msg:
        results = df[df['status'].str.contains('Ongoing', case=False)]
        formatted = f"Found {len(results)} Ongoing treatment patients:\n─────────────────────"
        for _, row in results.iterrows():
            formatted += f"""
👤 {row['name']} | Age: {row['age']}
🏥 {row['condition']}
⏳ Status: Ongoing
─────────────────────"""
        return {"response": formatted}

    else:
        return {"response": """🤖 Healthcare MCP Agent Ready!
─────────────────────
I can help you with:

🔬 'Show thyroid cancer patients'
📊 'Give me statistics'
👥 'Show patients age 30 to 50'
🏥 'Show all conditions'
💊 'Show diabetes patients'
❤️ 'Show heart disease patients'
🩺 'Show hypertension patients'
✅ 'Show recovered patients'
⏳ 'Show ongoing patients'
─────────────────────"""}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)