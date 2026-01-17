from __future__ import annotations

from engine.optimiser import generate_teams
from engine.types import DomainConfig, Participant


def main() -> None:
    # Temporary sample data (replace with CSV loader later)
    players = [
        Participant(id="adil", name="Adil", roles=("ST", "DF"), attributes={"speed": 5, "finishing": 8, "defending": 4, "stamina": 6}),
        Participant(id="forhid", name="Forhid", roles=("CM",), attributes={"speed": 6, "finishing": 6, "defending": 6, "stamina": 7}),
        Participant(id="sara", name="Sara", roles=("DF",), attributes={"speed": 6, "finishing": 3, "defending": 8, "stamina": 6}),
        Participant(id="mo", name="Mo", roles=("ST",), attributes={"speed": 7, "finishing": 7, "defending": 4, "stamina": 6}),
        Participant(id="lina", name="Lina", roles=("GK",), attributes={"speed": 4, "finishing": 2, "defending": 7, "stamina": 6}),
        Participant(id="jamal", name="Jamal", roles=("CM",), attributes={"speed": 7, "finishing": 5, "defending": 6, "stamina": 7}),
        Participant(id="aisha", name="Aisha", roles=("ST",), attributes={"speed": 8, "finishing": 7, "defending": 3, "stamina": 6}),
        Participant(id="rafi", name="Rafi", roles=("DF",), attributes={"speed": 6, "finishing": 4, "defending": 8, "stamina": 7}),
        Participant(id="noah", name="Noah", roles=("CM",), attributes={"speed": 6, "finishing": 6, "defending": 6, "stamina": 6}),
        Participant(id="zee", name="Zee", roles=("ST",), attributes={"speed": 7, "finishing": 8, "defending": 4, "stamina": 5}),
        Participant(id="hani", name="Hani", roles=("DF",), attributes={"speed": 5, "finishing": 3, "defending": 8, "stamina": 6}),
        Participant(id="omar", name="Omar", roles=("CM",), attributes={"speed": 6, "finishing": 5, "defending": 6, "stamina": 7}),
        Participant(id="tariq", name="Tariq", roles=("ST",), attributes={"speed": 7, "finishing": 7, "defending": 4, "stamina": 6}),
        Participant(id="nadia", name="Nadia", roles=("DF",), attributes={"speed": 6, "finishing": 4, "defending": 8, "stamina": 6}),
    ]

    cfg = DomainConfig(
        domain_name="football",
        team_size=7,
        attribute_weights={"speed": 0.30, "finishing": 0.35, "defending": 0.25, "stamina": 0.10},
        rating_weight=0.25,
        role_targets={"GK": 1, "DF": 2, "CM": 2, "ST": 2},
        seed=42,
        improve_swaps=100,
    )

    assignment = generate_teams(players, cfg)

    print("WhatsApp copy/paste:\n")
    print(f"Team A (strength {assignment.report.team_a_strength}, roles {assignment.report.team_a_roles})")
    for p in assignment.team_a:
        print(f"- {p.name} ({'/'.join(p.roles)})")
    print("")
    print(f"Team B (strength {assignment.report.team_b_strength}, roles {assignment.report.team_b_roles})")
    for p in assignment.team_b:
        print(f"- {p.name} ({'/'.join(p.roles)})")

    print("\nFairness:")
    print(f"- diff: {assignment.report.strength_diff} ({assignment.report.strength_diff_percent}%)")
    for n in assignment.report.notes:
        print(f"- {n}")


if __name__ == "__main__":
    main()
