from __future__ import annotations

from typing import Dict, Iterable, Tuple

from .types import DomainConfig, FairnessReport, Participant
from .scoring import compute_strengths


def _role_counts(team: Tuple[Participant, ...]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for p in team:
        for r in p.roles:
            ru = r.upper()
            counts[ru] = counts.get(ru, 0) + 1
    return counts


def _attribute_totals(team: Tuple[Participant, ...], cfg: DomainConfig) -> Dict[str, float]:
    totals = {k: 0.0 for k in cfg.attribute_weights.keys()}
    for p in team:
        for k in totals.keys():
            totals[k] += float(p.attributes.get(k, 0.0))
    return totals


def fairness_report(team_a: Tuple[Participant, ...], team_b: Tuple[Participant, ...], cfg: DomainConfig) -> FairnessReport:
    participants = tuple(team_a + team_b)
    strengths = compute_strengths(participants, cfg)

    a_strength = round(sum(strengths[p.id] for p in team_a), 6)
    b_strength = round(sum(strengths[p.id] for p in team_b), 6)
    diff = abs(a_strength - b_strength)
    avg = (a_strength + b_strength) / 2 if (a_strength + b_strength) else 0.0
    diff_pct = (diff / avg) * 100 if avg else 0.0

    notes = []
    if diff_pct <= 5:
        notes.append("Teams are very close (<= 5% strength difference).")
    elif diff_pct <= 10:
        notes.append("Teams are reasonably balanced (<= 10% strength difference).")
    else:
        notes.append("Teams may feel imbalanced (> 10% strength difference).")

    return FairnessReport(
        team_a_strength=round(a_strength, 3),
        team_b_strength=round(b_strength, 3),
        strength_diff=round(diff, 3),
        strength_diff_percent=round(diff_pct, 2),
        team_a_roles=_role_counts(team_a),
        team_b_roles=_role_counts(team_b),
        team_a_attribute_totals=_attribute_totals(team_a, cfg),
        team_b_attribute_totals=_attribute_totals(team_b, cfg),
        notes=tuple(notes),
    )
