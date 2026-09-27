"""Data models for Murder Mystery Engine."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Suspect(BaseModel):
    """An individual suspect with their stateful profile and secrets."""
    id: str
    name: str
    role: str
    bio: str
    personality: str
    alibi: str
    secret: str
    is_guilty: bool = False
    dialogue_history: List[Dict[str, str]] = Field(default_factory=list)


class Clue(BaseModel):
    """A physical, forensic, or testimonial piece of evidence."""
    id: str
    title: str
    description: str
    category: str  # physical, forensic, testimonial
    revealed: bool = False
    trigger_keywords: List[str] = Field(default_factory=list)


class MysteryDossier(BaseModel):
    """Ground truth and presentation dossier for a mystery case."""
    case_id: str
    title: str
    subtitle: str
    victim: str
    crime_scene: str
    time_of_death: str
    weapon_used: str
    synopsis: str
    suspects: List[Suspect]
    clues: List[Clue]
    true_culprit_id: str
    true_motive: str
    true_weapon: str


class InterrogationRequest(BaseModel):
    """Request payload for interrogating a suspect."""
    suspect_id: str
    question: str


class InterrogationResponse(BaseModel):
    """Response returned from interrogating a suspect."""
    suspect_id: str
    suspect_name: str
    answer: str
    clues_unlocked: List[Clue] = Field(default_factory=list)
    remaining_turns: int = 15


class AccusationRequest(BaseModel):
    """Payload when the detective formalizes an indictment."""
    accused_suspect_id: str
    accused_weapon: str
    motive_theory: str
    cited_clue_ids: List[str] = Field(default_factory=list)


class DetectiveScorecard(BaseModel):
    """Final assessment by the Truth Keeper agent."""
    is_solved: bool
    culprit_match: bool
    weapon_match: bool
    motive_score: int  # 0 to 40
    evidence_score: int  # 0 to 30
    total_score: int  # 0 to 100
    rank: str  # Master Detective, Senior Inspector, Deputy Sleuth, Rookie Constable, Cold Case Analyst
    verdict_summary: str
    ground_truth_culprit: str
    ground_truth_motive: str
    ground_truth_weapon: str
