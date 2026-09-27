"""FastAPI server for Murder Mystery Engine interactive web arena."""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.engine import ENGINE
from src.models import (
    InterrogationRequest,
    InterrogationResponse,
    AccusationRequest,
    DetectiveScorecard,
)
from src.scenarios import get_case_blackwood, get_case_silicon_valley

app = FastAPI(
    title="Murder Mystery Engine — AI Who-Dun-It",
    description="Stateful multi-agent murder mystery game powered by LangGraph",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active default session
CURRENT_SESSION = ENGINE.create_session("case_blackwood")


@app.get("/api/cases")
def list_cases():
    """List available murder mystery cases."""
    cases = [get_case_blackwood(), get_case_silicon_valley()]
    return [
        {
            "id": c.case_id,
            "title": c.title,
            "subtitle": c.subtitle,
            "victim": c.victim,
            "scene": c.crime_scene,
        }
        for c in cases
    ]


@app.get("/api/session")
def get_session_state(case_id: str = "case_blackwood"):
    """Get or reset active case state."""
    global CURRENT_SESSION
    if CURRENT_SESSION.case_id != case_id:
        CURRENT_SESSION = ENGINE.create_session(case_id)

    d = CURRENT_SESSION.dossier
    return {
        "session_id": CURRENT_SESSION.session_id,
        "case_id": d.case_id,
        "title": d.title,
        "subtitle": d.subtitle,
        "victim": d.victim,
        "crime_scene": d.crime_scene,
        "time_of_death": d.time_of_death,
        "synopsis": d.synopsis,
        "remaining_turns": CURRENT_SESSION.remaining_turns,
        "suspects": [
            {
                "id": s.id,
                "name": s.name,
                "role": s.role,
                "bio": s.bio,
                "personality": s.personality,
                "alibi": s.alibi,
            }
            for s in d.suspects
        ],
        "unlocked_clues": [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "category": c.category,
            }
            for c in CURRENT_SESSION.get_unlocked_clues()
        ],
    }


@app.post("/api/interrogate", response_model=InterrogationResponse)
def interrogate_suspect(req: InterrogationRequest):
    """Interrogate a suspect via LangGraph."""
    return CURRENT_SESSION.interrogate(req.suspect_id, req.question)


@app.get("/api/clues")
def get_clues():
    """Retrieve discovered clues."""
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "category": c.category,
        }
        for c in CURRENT_SESSION.get_unlocked_clues()
    ]


@app.post("/api/accuse", response_model=DetectiveScorecard)
def submit_accusation(req: AccusationRequest):
    """Submit formal indictment to Truth Keeper agent."""
    return CURRENT_SESSION.accuse(req)


# Static assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
