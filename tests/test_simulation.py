"""End-to-end simulation runner test."""

from src.cli import run_demo_simulation


def test_full_game_simulation_run():
    """Verify that a complete playthrough simulation executes cleanly."""
    output = run_demo_simulation("case_blackwood")
    assert "DETECTIVE SIMULATION" in output
    assert "CRIME SCENE BRIEFING" in output
    assert "PHASE 5: COURT OF FORMAL ACCUSATION" in output
    assert "SIMULATION RUN COMPLETED WITH ZERO ERRORS" in output
    assert "SOLVED" in output
