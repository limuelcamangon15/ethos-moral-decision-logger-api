import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_decision(context, action, reasoning):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Analyze the decision and return ONLY JSON:

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