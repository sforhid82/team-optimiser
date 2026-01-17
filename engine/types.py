from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple


Attributes = Dict[str, float]


@dataclass(frozen=True)
class Participant:
    """
    Framework-agnostic representation of a player/participant.
    Keep this pure; Django will map into/out of this later.
    """
    id: str
    name: str
    roles: Tuple[str, ...] = ()
    attributes: Attributes = field(default_factory=dict)
    rating: float = 1000.0
    notes: str = ""

    def has_role(self, role: str) -> bool:
        role_u = role.upper()
        return any(r.upper() == role_u for r in self.roles)


@dataclass(frozen=True)
class DomainConfig:
    """
    Tuning knobs for the engine.
    - attribute_weights: how to turn attributes into a base skill score
    - rating_weight: how much the learned rating contributes
    - role_targets: soft constraints like "try to put 1 GK per team"
    - seed: deterministic output for the same input
    - improve_swaps: number of random swap attempts to try improving fairness
    """
    domain_name: str = "football"
    team_size: int = 7
    attribute_weights: Dict[str, float] = field(default_factory=dict)
    rating_weight: float = 0.25
    role_targets: Dict[str, int] = field(default_factory=dict)
    seed: int = 42
    improve_swaps: int = 80

    def normalised_role_targets(self) -> Dict[str, int]:
        return {k.upper(): int(v) for k, v in self.role_targets.items()}


class MatchResult(str, Enum):
    A_WIN = "A_WIN"
    B_WIN = "B_WIN"
    DRAW = "DRAW"


@dataclass(frozen=True)
class Outcome:
    result: MatchResult
    team_a_score: Optional[int] = None
    team_b_score: Optional[int] = None
    felt_balanced: Optional[bool] = None


@dataclass(frozen=True)
class TeamAssignment:
    team_a: Tuple[Participant, ...]
    team_b: Tuple[Participant, ...]
    report: "FairnessReport"


@dataclass(frozen=True)
class FairnessReport:
    team_a_strength: float
    team_b_strength: float
    strength_diff: float
    strength_diff_percent: float
    team_a_roles: Dict[str, int]
    team_b_roles: Dict[str, int]
    team_a_attribute_totals: Dict[str, float]
    team_b_attribute_totals: Dict[str, float]
    notes: Tuple[str, ...] = ()


@dataclass(frozen=True)
class SessionRecord:
    """
    Optional: Useful later when you persist sessions.
    Not used by the optimiser directly.
    """
    session_id: str
    session_date: date
    participant_ids: Tuple[str, ...]
