"""Tests for suspect memory retention and personas."""

import pytest
from src.engine import ENGINE


def test_suspect_interrogation_memory():
    """Verify that suspects maintain dialogue history across turns."""
    session = ENGINE.create_session("case_blackwood")
    suspect = session.get_suspect("doctor_finch")
    assert suspect is not None
    assert len(suspect.dialogue_history) == 0

    resp1 = session.interrogate("doctor_finch", "Did you examine the port wine?")
    assert len(resp1.answer) > 0
    assert len(suspect.dialogue_history) == 2  # question + answer

    resp2 = session.interrogate("doctor_finch", "Why are your hands trembling?")
    assert len(resp2.answer) > 0
    assert len(suspect.dialogue_history) == 4


def test_multiple_suspect_isolation():
    """Verify that different suspect memory state remains isolated."""
    session = ENGINE.create_session("case_blackwood")
    session.interrogate("butler_arthur", "What was on the silver tray?")
    session.interrogate("heiress_beatrice", "Were you sketching in the garden?")

    arthur = session.get_suspect("butler_arthur")
    beatrice = session.get_suspect("heiress_beatrice")

    assert len(arthur.dialogue_history) == 2
    assert len(beatrice.dialogue_history) == 2
    assert arthur.dialogue_history[0]["text"] == "What was on the silver tray?"
    assert beatrice.dialogue_history[0]["text"] == "Were you sketching in the garden?"
