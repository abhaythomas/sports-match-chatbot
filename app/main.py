from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="Sports Match Chatbot API", version="0.1.0")

MOCK_MATCHES = [
    {
        "match_id": "1",
        "league": "Bundesliga",
        "home": "Bayern Munich",
        "away": "Borussia Dortmund",
        "status": "upcoming",
        "kickoff_utc": "2026-02-19T18:30:00Z",
    },
    {
        "match_id": "2",
        "league": "Bundesliga",
        "home": "RB Leipzig",
        "away": "Bayer Leverkusen",
        "status": "live",
        "score": "1-0",
        "minute": 52,
        "kickoff_utc": "2026-02-19T16:30:00Z",
    },
    {
        "match_id": "3",
        "league": "Bundesliga",
        "home": "Stuttgart",
        "away": "Frankfurt",
        "status": "finished",
        "score": "2-2",
        "kickoff_utc": "2026-02-18T18:30:00Z",
    },
]

def get_match(match_id: str):
    return next((m for m in MOCK_MATCHES if m["match_id"] == match_id), None)

@app.get("/health")
def health():
    return {"ok": True, "time_utc": datetime.now(timezone.utc).isoformat()}

@app.get("/matches/live")
def live_matches(league: str = "Bundesliga"):
    return [m for m in MOCK_MATCHES if m["league"] == league and m["status"] == "live"]

@app.get("/matches/today")
def today_matches(league: str = "Bundesliga"):
    return [m for m in MOCK_MATCHES if m["league"] == league]

@app.get("/match/{match_id}/preview")
def match_preview(match_id: str):
    m = get_match(match_id)
    if not m:
        return {"error": "match not found"}

    preview = (
        f"{m['home']} vs {m['away']} ({m['league']})\n"
        f"Kickoff (UTC): {m['kickoff_utc']}\n"
        f"Status: {m['status']}\n"
    )
    if m.get("score"):
        preview += f"Current/Final score: {m['score']}\n"
    if m.get("minute"):
        preview += f"Minute: {m['minute']}\n"

    preview += "\nWhat to watch (MVP):\n- Team news/lineups\n- Momentum swings\n- Set pieces\n"

    return {"match_id": match_id, "preview": preview}

@app.get("/match/{match_id}/summary")
def match_summary(match_id: str):
    m = get_match(match_id)
    if not m:
        return {"error": "match not found"}

    score = m.get("score", "Score not available")
    summary = (
        f"{m['home']} {score} {m['away']}\n"
        f"League: {m['league']}\n"
        f"Status: {m['status']}\n\n"
        "Summary (MVP): This will become an AI-generated summary once we plug in real events + an LLM."
    )

    return {"match_id": match_id, "summary": summary}
