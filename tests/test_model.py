import pytest
from geroscience_evidence import Candidate, Evidence, EvidenceEngine


def e(source="a", species="mouse", design="multisite", effect=.7, uncertainty=.2, replication=.8, safety=.7, hallmarks=("h1",)):
    return Evidence(source, species, design, effect, uncertainty, replication, safety, hallmarks)


def test_high_quality_human_evidence_scores_above_cell_evidence():
    engine = EvidenceEngine()
    human = Candidate("human", (e(species="human", design="randomized"),))
    cell = Candidate("cell", (e(species="cell", design="in_vitro"),))
    assert engine.score(human).priority > engine.score(cell).priority


def test_uncertainty_reduces_priority():
    engine = EvidenceEngine()
    certain = Candidate("certain", (e(uncertainty=.05),))
    uncertain = Candidate("uncertain", (e(uncertainty=.9),))
    assert engine.score(certain).priority > engine.score(uncertain).priority


def test_safety_changes_priority_without_erasing_evidence():
    engine = EvidenceEngine()
    safe = engine.score(Candidate("safe", (e(safety=.95),)))
    risky = engine.score(Candidate("risky", (e(safety=.1),)))
    assert safe.evidence_score == pytest.approx(risky.evidence_score)
    assert safe.priority > risky.priority


def test_hallmark_coverage_is_bounded():
    score = EvidenceEngine(total_hallmarks=2).score(Candidate("broad", (e(hallmarks=("a","b","c")),)))
    assert score.hallmark_coverage == 1


def test_bootstrap_is_reproducible():
    candidate = Candidate("repeat", (e("a"), e("b", effect=.4)))
    engine = EvidenceEngine(seed=3)
    assert engine.score(candidate).interval_90 == engine.score(candidate).interval_90


def test_leave_one_source_out_penalizes_fragile_candidates():
    stable = Candidate("stable", (e("a", effect=.7), e("b", effect=.72), e("c", effect=.68)))
    fragile = Candidate("fragile", (e("a", effect=.95), e("b", effect=.1), e("c", effect=.1)))
    engine = EvidenceEngine()
    assert engine.score(stable).robustness > engine.score(fragile).robustness


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        EvidenceEngine().score(Candidate("bad", (e(effect=1.2),)))


def test_ranking_orders_by_priority():
    engine = EvidenceEngine()
    results = engine.rank([Candidate("low", (e(effect=.2),)), Candidate("high", (e(effect=.9),))])
    assert [result.name for result in results] == ["high", "low"]
