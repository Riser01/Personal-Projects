"""Tests for Truth Keeper accusation scoring."""

import pytest
from src.engine import ENGINE
from src.models import AccusationRequest


def test_correct_accusation_scoring():
    """Verify that accurate indictment receives maximum points and Master Detective rank."""
    session = ENGINE.create_session("case_blackwood")
    # Unlock clues first
    session.interrogate("doctor_finch", "Did you prescribe Wolfsbane poison?")
    session.interrogate("doctor_finch", "Tell me about the medical malpractice letter.")

    accusation = AccusationRequest(
        accused_suspect_id="doctor_finch",
        accused_weapon="Aconite Wolfsbane poison",
        motive_theory="Dr. Finch killed Lord Reginald to prevent evidence of medical malpractice and murder from reaching authorities",
        cited_clue_ids=session.unlocked_clue_ids,
    )

    scorecard = session.accuse(accusation)
    assert scorecard.is_solved is True
    assert scorecard.culprit_match is True
    assert scorecard.weapon_match is True
    assert scorecard.total_score >= 80
    assert "Master Detective" in scorecard.rank or "Senior Inspector" in scorecard.rank


def test_incorrect_culprit_fails_case():
    """Verify that accusing an innocent person fails the case."""
    session = ENGINE.create_session("case_blackwood")
    accusation = AccusationRequest(
        accused_suspect_id="butler_arthur",
        accused_weapon="Pistol",
        motive_theory="Arthur wanted to steal the family silverware",
        cited_clue_ids=[],
    )

    scorecard = session.accuse(accusation)
    assert scorecard.is_solved is False
    assert scorecard.culprit_match is False
    assert scorecard.total_score < 40
    assert "Rookie Constable" in scorecard.rank or "Cold Case" in scorecard.rank
