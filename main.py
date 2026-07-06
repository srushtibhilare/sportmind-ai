from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from database import get_connection
from ai import get_coaching_advice

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SportMind AI is running. Try /analyze?player=Virat Kohli"}


@app.get("/analyze")
def analyze(player: str = Query(...)):
    matches = []

    with open("sample_matches.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["player"].lower() == player.lower():
                matches.append(row)

    if not matches:
        return {"error": "No data found for this player."}

    total_runs = sum(int(m["runs"]) for m in matches)
    total_balls = sum(int(m["balls"]) for m in matches)

    average_runs = total_runs / len(matches)
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    if average_runs >= 40:
        insight = "Good recent batting form."
    elif average_runs >= 20:
        insight = "Average form, needs consistency."
    else:
        insight = "Poor recent form, needs improvement."

    # --- Fetch previous analysis for this player BEFORE saving the new one ---
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT average_runs, strike_rate, insight, created_at
        FROM analyses
        WHERE player_name = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (player,))

    previous = cur.fetchone()

    previous_analysis = None
    if previous:
        previous_analysis = {
            "average_runs": previous[0],
            "strike_rate": previous[1],
            "insight": previous[2],
            "created_at": str(previous[3])
        }

    # --- Save the new analysis into CockroachDB ---
    cur.execute("""
        INSERT INTO analyses (player_name, average_runs, strike_rate, insight)
        VALUES (%s, %s, %s, %s)
    """, (player, average_runs, strike_rate, insight))

    conn.commit()
    cur.close()
    conn.close()

    # --- Generate AI coaching advice ---
    ai_advice = get_coaching_advice(player, average_runs, strike_rate, insight, previous_analysis)

    return {
        "player": player,
        "matches_analyzed": len(matches),
        "average_runs": round(average_runs, 2),
        "strike_rate": round(strike_rate, 2),
        "insight": insight,
        "previous_analysis": previous_analysis,
        "ai_advice": ai_advice
    }