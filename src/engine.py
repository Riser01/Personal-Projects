"""High-level Game Engine coordinating Mystery Game Sessions and LangGraph."""

import uuid
from typing import Dict, Optional, List, Tuple
from src.models import (
    MysteryDossier,
    Suspect,
    Clue,
    InterrogationResponse,
    AccusationRequest,
    DetectiveScorecard,
)
from src.scenarios import load_scenario
from src.graph import (
    MysteryState,
    build_interrogation_graph,
    build_accusation_graph,
)


class GameSession:
    """An active mystery investigation session."""

    def __init__(self, session_id: str, case_id: str = "case_blackwood"):
        self.session_id = session_id
        self.case_id = case_id
        self.dossier: MysteryDossier = load_scenario(case_id)
        self.unlocked_clue_ids: List[str] = []
        self.interrogation_history: List[Dict[str, str]] = []
        self.remaining_turns: int = 15
        self.scorecard: Optional[DetectiveScorecard] = None

        self._interrogation_graph = build_interrogation_graph()
        self._accusation_graph = build_accusation_graph()

    def get_suspect(self, suspect_id: str) -> Optional[Suspect]:
        for s in self.dossier.suspects:
            if s.id == suspect_id:
                return s
        return None

    def get_unlocked_clues(self) -> List[Clue]:
        return [c for c in self.dossier.clues if c.id in self.unlocked_clue_ids]

    def interrogate(self, suspect_id: str, question: str) -> InterrogationResponse:
        """Run an interrogation turn through LangGraph."""
        if self.remaining_turns <= 0:
            return InterrogationResponse(
                suspect_id=suspect_id,
                suspect_name="Constable on Duty",
                answer="Investigation window closed! You have exhausted your interrogation permits. You must formalize your accusation now.",
                clues_unlocked=[],
                remaining_turns=0,
            )

        state: MysteryState = {
            "dossier": self.dossier,
            "active_suspect_id": suspect_id,
            "current_question": question,
            "current_answer": "",
            "interrogation_history": self.interrogation_history,
            "unlocked_clue_ids": self.unlocked_clue_ids,
            "newly_unlocked_clue_ids": [],
            "accusation": None,
            "scorecard": None,
            "remaining_turns": self.remaining_turns,
            "status": "start",
        }

        result = self._interrogation_graph.invoke(state)

        # Update session state from LangGraph node outputs
        self.remaining_turns = result.get("remaining_turns", self.remaining_turns - 1)
        self.unlocked_clue_ids = result.get("unlocked_clue_ids", self.unlocked_clue_ids)
        self.interrogation_history = result.get("interrogation_history", self.interrogation_history)

        newly_unlocked = [
            c for c in self.dossier.clues if c.id in result.get("newly_unlocked_clue_ids", [])
        ]

        suspect = self.get_suspect(suspect_id)
        suspect_name = suspect.name if suspect else suspect_id

        return InterrogationResponse(
            suspect_id=suspect_id,
            suspect_name=suspect_name,
            answer=result.get("current_answer", "No comment."),
            clues_unlocked=newly_unlocked,
            remaining_turns=self.remaining_turns,
        )

    def accuse(self, accusation: AccusationRequest) -> DetectiveScorecard:
        """Submit formal accusation and score via Truth Keeper agent."""
        state: MysteryState = {
            "dossier": self.dossier,
            "active_suspect_id": "",
            "current_question": "",
            "current_answer": "",
            "interrogation_history": self.interrogation_history,
            "unlocked_clue_ids": self.unlocked_clue_ids,
            "newly_unlocked_clue_ids": [],
            "accusation": accusation,
            "scorecard": None,
            "remaining_turns": self.remaining_turns,
            "status": "accusing",
        }

        result = self._accusation_graph.invoke(state)
        scorecard = result.get("scorecard")
        self.scorecard = scorecard
        return scorecard


class EngineManager:
    """Manages active game sessions."""

    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}

    def create_session(self, case_id: str = "case_blackwood") -> GameSession:
        session_id = str(uuid.uuid4())[:8]
        session = GameSession(session_id, case_id)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[GameSession]:
        return self.sessions.get(session_id)


# Global singleton engine
ENGINE = EngineManager()
