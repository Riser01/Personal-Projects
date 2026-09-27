"""Tests for dynamic clue dropper agent."""

import pytest
from src.engine import ENGINE


def test_clue_unlocking_triggers():
    """Verify that asking keyword-relevant questions unlocks forensic clues."""
    session = ENGINE.create_session("case_blackwood")
    assert len(session.unlocked_clue_ids) == 0

    # Ask an un-related question
    session.interrogate("butler_arthur", "What color is the library wallpaper?")
    assert len(session.unlocked_clue_ids) == 0

    # Ask about prescription and doctor's clinic
    resp = session.interrogate("doctor_finch", "Did you prescribe medicine or drugs from your clinic?")
    assert len(resp.clues_unlocked) >= 1
    unlocked_ids = [c.id for c in resp.clues_unlocked]
    assert "clue_apothecary_ledger" in unlocked_ids
    assert "clue_apothecary_ledger" in session.unlocked_clue_ids


def test_no_duplicate_clue_unlocks():
    """Verify that already unlocked clues are not re-triggered."""
    session = ENGINE.create_session("case_blackwood")
    session.interrogate("doctor_finch", "Did you examine the port wine and poison?")
    count_first = len(session.unlocked_clue_ids)
    assert count_first >= 1

    # Ask identical trigger again
    resp2 = session.interrogate("doctor_finch", "Tell me more about the port wine and glass.")
    assert len(resp2.clues_unlocked) == 0  # Not re-unlocked
