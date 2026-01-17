from __future__ import annotations

import random
from typing import Dict, List, Tuple

from .metrics import fairness_report
from .scoring import compute_strengths
from .types import DomainConfig, Participant, TeamAssignment


def _team_total_strength(team: Tuple[Participant, ...], strengths: Dict[str, float]) -> float:
    return sum(strengths[p.id] for p in team)


def _team_role_counts(team: Tuple[Participant, ...]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for p in team:
        for r in p.roles:
            ru = r.upper()
            counts[ru] = counts.get(ru, 0) + 1
    return counts


def _role_need_delta(role: str, team_counts: Dict[str, int], target: int) -> int:
    """
    Positive means team still needs this role to hit its target.
    """
    return max(0, target - team_counts.get(role, 0))


def generate_teams(participants: List[Participant], cfg: DomainConfig) -> TeamAssignment:
    team_size = int(cfg.team_size)
    needed = 2 * team_size
    if len(participants) < needed:
        raise ValueError(f"Need at least {needed} participants for {team_size}v{team_size}, got {len(participants)}.")

    # Deterministic selection and deterministic shuffle based on seed
    rng = random.Random(cfg.seed)

    # If more than needed, choose a deterministic sample (sorted by id then sample)
    parts_sorted = sorted(participants, key=lambda p: (p.id, p.name))
    if len(parts_sorted) > needed:
        # deterministic sample
        parts_sorted = rng.sample(parts_sorted, k=needed)

    parts = tuple(parts_sorted)
    strengths = compute_strengths(parts, cfg)

    # Sort strongest first for greedy allocation
    ranked = sorted(parts, key=lambda p: strengths[p.id], reverse=True)

    role_targets = cfg.normalised_role_targets()

    team_a: List[Participant] = []
    team_b: List[Participant] = []

    for p in ranked:
        # size guards
        if len(team_a) >= team_size:
            team_b.append(p)
            continue
        if len(team_b) >= team_size:
            team_a.append(p)
            continue

        a_tuple = tuple(team_a)
        b_tuple = tuple(team_b)

        a_total = _team_total_strength(a_tuple, strengths)
        b_total = _team_total_strength(b_tuple, strengths)

        a_roles = _team_role_counts(a_tuple)
        b_roles = _team_role_counts(b_tuple)

        # Base choice: put into weaker team
        choose_a = a_total <= b_total

        # Soft nudge: if one team needs this player's roles more, prefer it
        # (Pick the strongest single role need effect)
        best_role_bias = 0  # positive -> choose A, negative -> choose B
        for r in p.roles:
            ru = r.upper()
            if ru in role_targets:
                need_a = _role_need_delta(ru, a_roles, role_targets[ru])
                need_b = _role_need_delta(ru, b_roles, role_targets[ru])
                bias = need_a - need_b
                if abs(bias) > abs(best_role_bias):
                    best_role_bias = bias

        if best_role_bias > 0:
            choose_a = True
        elif best_role_bias < 0:
            choose_a = False

        (team_a if choose_a else team_b).append(p)

    # Optional improvement pass: try random swaps to reduce strength diff
    team_a_t = tuple(team_a)
    team_b_t = tuple(team_b)
    best_a, best_b = _improve_by_swaps(team_a_t, team_b_t, strengths, cfg, rng)

    report = fairness_report(best_a, best_b, cfg)
    return TeamAssignment(team_a=best_a, team_b=best_b, report=report)


def _imbalance_cost(team_a: Tuple[Participant, ...], team_b: Tuple[Participant, ...], strengths: Dict[str, float]) -> float:
    # Cost = absolute difference in total strengths
    return abs(_team_total_strength(team_a, strengths) - _team_total_strength(team_b, strengths))


def _improve_by_swaps(
    team_a: Tuple[Participant, ...],
    team_b: Tuple[Participant, ...],
    strengths: Dict[str, float],
    cfg: DomainConfig,
    rng: random.Random,
) -> Tuple[Tuple[Participant, ...], Tuple[Participant, ...]]:
    swaps = max(0, int(cfg.improve_swaps))
    if swaps == 0:
        return team_a, team_b

    best_a = list(team_a)
    best_b = list(team_b)
    best_cost = _imbalance_cost(tuple(best_a), tuple(best_b), strengths)

    for _ in range(swaps):
        i = rng.randrange(len(best_a))
        j = rng.randrange(len(best_b))

        cand_a = best_a.copy()
        cand_b = best_b.copy()
        cand_a[i], cand_b[j] = cand_b[j], cand_a[i]

        cost = _imbalance_cost(tuple(cand_a), tuple(cand_b), strengths)
        if cost < best_cost:
            best_a, best_b = cand_a, cand_b
            best_cost = cost

    return tuple(best_a), tuple(best_b)
