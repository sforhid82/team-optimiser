from __future__ import annotations

from typing import Dict, Iterable, Tuple

from .types import DomainConfig, Participant


def attribute_score(p: Participant, cfg: DomainConfig) -> float:
    # Weighted sum of declared attributes (missing attributes are treated as 0)
    total = 0.0
    for attr, w in cfg.attribute_weights.items():
        total += float(p.attributes.get(attr, 0.0)) * float(w)
    return total


def normalise_ratings(participants: Tuple[Participant, ...]) -> Dict[str, float]:
    """
    Map ratings to a stable 0..1 range within the session so it doesn't dominate.
    If all ratings equal, everyone gets 0.5.
    """
    ratings = [p.rating for p in participants]
    r_min = min(ratings)
    r_max = max(ratings)
    if r_max == r_min:
        return {p.id: 0.5 for p in participants}
    return {p.id: (p.rating - r_min) / (r_max - r_min) for p in participants}


def overall_strength(p: Participant, cfg: DomainConfig, rating_norm: float) -> float:
    # rating_norm is 0..1; rating_weight controls how influential learning is
    base = attribute_score(p, cfg)
    return base + (cfg.rating_weight * rating_norm)


def compute_strengths(participants: Tuple[Participant, ...], cfg: DomainConfig) -> Dict[str, float]:
    norm = normalise_ratings(participants)
    return {p.id: overall_strength(p, cfg, norm[p.id]) for p in participants}
