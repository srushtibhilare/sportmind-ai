# 🏏 SportMind AI

**An AI cricket performance coach with long-term memory.**

SportMind AI analyzes real IPL player statistics, remembers every past analysis, and generates personalized coaching advice using a large language model — combining relational data, persistent memory, and generative AI into one agent.

---

## What it does

1. Enter a player name (e.g. `V Kohli`, `CH Gayle`, `MS Dhoni`).
2. The backend calculates real performance stats — average runs, strike rate, and current form — from actual IPL ball-by-ball match data.
3. It checks **CockroachDB** for any previous analysis of that player and recalls it.
4. It sends the current stats *and* the recalled memory to an **LLM (Llama 3.1 via Hugging Face)**, which generates a short, contextual coaching note — comparing current form to past performance.
5. The new analysis is saved back into CockroachDB, so the agent gets smarter about that player every time it's asked again.

This is the core idea: **the agent is useful because it remembers.** A player analyzed today is compared against their own history the next time someone asks about them.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database / Memory | CockroachDB (Serverless, free tier) |
| AI | Llama 3.1 (via Hugging Face Inference API) |
| Data | [Cricsheet](https://cricsheet.org) — real ball-by-ball IPL match data (1,243+ matches) |
| Frontend | HTML, CSS, vanilla JavaScript |

---

## Project structure
