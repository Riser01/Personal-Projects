"""Tests for LangGraph state machine and node executions."""

import pytest
from src.scenarios import load_scenario
from src.graph import (
    MysteryState,
    build_interrogation_graph,
    build_accusation_graph,
)
from src.models import AccusationRequest


def test_interrogation_graph_turn():
    """Verify that an interrogation turn executes through LangGraph nodes."""
    dossier = load_scenario("case_blackwood")
    graph = build_interrogation_graph()

    initial_state: MysteryState = {
        "dossier": dossier,
        "active_suspect_id": "butler_arthur",
        "current_question": "Where were you at 10 PM?",
        "current_answer": "",
        "interrogation_history": [],
        "unlocked_clue_ids": [],
        "newly_unlocked_clue_ids": [],
        "accusation": None,
        "scorecard": None,
        "remaining_turns": 15,
        "status": "start",
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "clues_evaluated"
    assert result["remaining_turns"] == 14
    assert len(result["current_answer"]) > 10
    assert len(result["interrogation_history"]) == 1
    assert result["interrogation_history"][0]["suspect_id"] == "butler_arthur"


def test_accusation_graph_execution():
    """Verify that formal accusation is evaluated by Truth Keeper node."""
    dossier = load_scenario("case_blackwood")
    graph = build_accusation_graph()

    accusation = AccusationRequest(
        accused_suspect_id="doctor_finch",
        accused_weapon="Aconite wolfsbane poison",
        motive_theory="Dr. Finch committed medical malpractice regarding Lady Blackwood",
        cited_clue_ids=["clue_wolfsbane", "clue_blackmail_draft"],
    )

    state: MysteryState = {
        "dossier": dossier,
        "active_suspect_id": "",
        "current_question": "",
        "current_answer": "",
        "interrogation_history": [],
        "unlocked_clue_ids": ["clue_wolfsbane", "clue_blackmail_draft"],
        "newly_unlocked_clue_ids": [],
        "accusation": accusation,
        "scorecard": None,
        "remaining_turns": 10,
        "status": "accusing",
    }

    result = graph.invoke(state)

    assert result["status"] == "indicted"
    scorecard = result["scorecard"]
    assert scorecard is not None
    assert scorecard.culprit_match is True
    assert scorecard.weapon_match is True
    assert scorecard.total_score >= 80
    assert scorecard.is_solved is True
