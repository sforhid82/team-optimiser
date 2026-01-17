from engine.optimiser import generate_teams
from engine.types import DomainConfig, Participant


def sample_players():
    return [
        Participant(id="a", name="A", roles=("ST",), attributes={"speed": 8, "finishing": 8, "defending": 2, "stamina": 6}),
        Participant(id="b", name="B", roles=("DF",), attributes={"speed": 5, "finishing": 3, "defending": 9, "stamina": 7}),
        Participant(id="c", name="C", roles=("CM",), attributes={"speed": 6, "finishing": 6, "defending": 6, "stamina": 6}),
        Participant(id="d", name="D", roles=("GK",), attributes={"speed": 4, "finishing": 2, "defending": 8, "stamina": 6}),
        Participant(id="e", name="E", roles=("ST",), attributes={"speed": 7, "finishing": 7, "defending": 4, "stamina": 6}),
        Participant(id="f", name="F", roles=("DF",), attributes={"speed": 6, "finishing": 4, "defending": 8, "stamina": 7}),
        Participant(id="g", name="G", roles=("CM",), attributes={"speed": 6, "finishing": 5, "defending": 6, "stamina": 7}),
        Participant(id="h", name="H", roles=("ST",), attributes={"speed": 7, "finishing": 8, "defending": 3, "stamina": 5}),
        Participant(id="i", name="I", roles=("DF",), attributes={"speed": 5, "finishing": 3, "defending": 8, "stamina": 6}),
        Participant(id="j", name="J", roles=("CM",), attributes={"speed": 6, "finishing": 6, "defending": 6, "stamina": 6}),
    ]


def cfg(team_size=5):
    return DomainConfig(
        team_size=team_size,
        attribute_weights={"speed": 0.30, "finishing": 0.35, "defending": 0.25, "stamina": 0.10},
        rating_weight=0.25,
        role_targets={"GK": 1, "DF": 1, "CM": 1, "ST": 1},
        seed=123,
        improve_swaps=60,
    )


def test_deterministic_output():
    players = sample_players()
    a1 = generate_teams(players, cfg())
    a2 = generate_teams(players, cfg())
    assert [p.id for p in a1.team_a] == [p.id for p in a2.team_a]
    assert [p.id for p in a1.team_b] == [p.id for p in a2.team_b]


def test_team_sizes_correct():
    players = sample_players()
    out = generate_teams(players, cfg(team_size=5))
    assert len(out.team_a) == 5
    assert len(out.team_b) == 5


def test_balance_reasonable():
    players = sample_players()
    out = generate_teams(players, cfg(team_size=5))
    # We don't demand perfection; we want a reasonable bound for the sample.
    assert out.report.strength_diff_percent < 20
