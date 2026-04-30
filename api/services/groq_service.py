import requests
import os
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_decision(context, action, reasoning):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
        Analyze this decision and return ONLY valid JSON.

        DO NOT include any text outside JSON.
        DO NOT wrap in backticks.

        Use ONLY these values:
    
        ethics: low, neutral, high  
        risk_level: low, medium, high  
        time_scope: short-term, long-term  
        affected_party: self, family, friends, peers, public

        Context: {context}
        Action: {action}
        Reasoning: {reasoning}

        Return JSON with:
        ethics, risk_level, time_scope, affected_party, justification_quality, confidence, explanation
        """

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        output = response.json()
        return output["choices"][0]["message"]["content"]
    except Exception:
        return {"error": "AI failed"}

# parses ai response into JSON format   
def parse_ai_response(content):
    try:
        cleaned = content.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)
    except Exception:
        return None