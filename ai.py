import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"

def get_coaching_advice(player_name, average_runs, strike_rate, insight, previous_analysis=None):

    memory_context = ""
    if previous_analysis:
        memory_context = f"""
Previous analysis for this player:
- Average runs: {previous_analysis['average_runs']}
- Strike rate: {previous_analysis['strike_rate']}
- Insight: {previous_analysis['insight']}

Compare current performance to this previous analysis.
"""
    else:
        memory_context = "This is the first recorded analysis for this player."

    prompt = f"""You are a professional cricket performance coach.

Current player stats:
- Player: {player_name}
- Average runs: {average_runs}
- Strike rate: {strike_rate}
- Basic insight: {insight}

{memory_context}

Give a short coaching response with:
1. One line on current form
2. One line about historical comparison (only if previous data exists, otherwise mention this is a fresh analysis)
3. One specific training tip
Keep the entire response under 80 words."""

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct:fastest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            return f"(AI temporarily unavailable: {result['error']})"
        else:
            return f"(AI response format unexpected: {result})"

    except Exception as e:
        return f"(AI error: {str(e)})"