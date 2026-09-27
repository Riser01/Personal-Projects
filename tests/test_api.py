"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_get_cases():
    """Verify endpoint listing available cases."""
    response = client.get("/api/cases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    case_ids = [c["id"] for c in data]
    assert "case_blackwood" in case_ids
    assert "case_silicon_valley" in case_ids


def test_get_session():
    """Verify session initialization endpoint."""
    response = client.get("/api/session?case_id=case_blackwood")
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "case_blackwood"
    assert len(data["suspects"]) == 3
    assert data["remaining_turns"] == 15


def test_interrogate_api():
    """Verify interrogation POST endpoint."""
    payload = {
        "suspect_id": "doctor_finch",
        "question": "Did you administer wolfsbane poison in the port wine?",
    }
    response = client.post("/api/interrogate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["suspect_id"] == "doctor_finch"
    assert len(data["answer"]) > 0
    assert data["remaining_turns"] < 15


def test_accuse_api():
    """Verify formal accusation POST endpoint."""
    payload = {
        "accused_suspect_id": "doctor_finch",
        "accused_weapon": "Wolfsbane poison",
        "motive_theory": "Concealing malpractice in Lady Blackwood's autopsy",
        "cited_clue_ids": ["clue_wolfsbane"],
    }
    response = client.post("/api/accuse", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_solved" in data
    assert "total_score" in data
    assert data["culprit_match"] is True
