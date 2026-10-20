"""Transparent evidence synthesis for preclinical geroscience prioritization."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
import random
from statistics import mean


SPECIES_TRANSLATION = {"cell": 0.22, "worm": 0.32, "fly": 0.38, "mouse": 0.62, "primate": 0.78, "human": 1.0}
DESIGN_QUALITY = {"in_vitro": 0.28, "observational": 0.42, "single_site": 0.55, "multisite": 0.78, "randomized": 1.0}


@dataclass(frozen=True)
class Evidence:
    source_id: str
    species: str
    design: str
    effect: float
    uncertainty: float
    replication: float
    safety: float
    hallmarks: tuple[str, ...] = ()

    def validate(self) -> None:
        if self.species not in SPECIES_TRANSLATION or self.design not in DESIGN_QUALITY:
            raise ValueError("unknown species or study design")
        for value in (self.effect, self.uncertainty, self.replication, self.safety):
            if not 0 <= value <= 1:
                raise ValueError("evidence inputs must lie in [0, 1]")


@dataclass(frozen=True)
class Candidate:
    name: str
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class CandidateScore:
    name: str
    evidence_score: float
    translation_score: float
    safety_score: float
    hallmark_coverage: float
    priority: float
    interval_90: tuple[float, float]
    robustness: float


class EvidenceEngine:
    """Reliability-weighted evidence aggregation with bootstrap uncertainty."""

    def __init__(self, total_hallmarks: int = 12, seed: int = 19):
        self.total_hallmarks = total_hallmarks
        self.seed = seed

    @staticmethod
    def _row_score(row: Evidence) -> tuple[float, float]:
        row.validate()
        reliability = DESIGN_QUALITY[row.design] * row.replication * (1 - 0.65 * row.uncertainty)
        translation = SPECIES_TRANSLATION[row.species]
        return row.effect * reliability, reliability * translation

    def _aggregate(self, rows: tuple[Evidence, ...]) -> tuple[float, float, float, float, float]:
        if not rows:
            raise ValueError("candidate needs evidence")
        scored = [self._row_score(row) for row in rows]
        weights = [max(weight, 1e-6) for _, weight in scored]
        evidence_score = sum(score * weight for (score, _), weight in zip(scored, weights)) / sum(weights)
        translation = sum(SPECIES_TRANSLATION[row.species] * weight for row, weight in zip(rows, weights)) / sum(weights)
        safety = sum(row.safety * weight for row, weight in zip(rows, weights)) / sum(weights)
        coverage = min(1.0, len({hallmark for row in rows for hallmark in row.hallmarks}) / self.total_hallmarks)
        diversity = min(1.0, len({row.species for row in rows}) / 3) * min(1.0, len({row.source_id for row in rows}) / 3)
        priority = evidence_score * (0.42 + 0.28 * translation + 0.18 * safety + 0.07 * coverage + 0.05 * diversity)
        return evidence_score, translation, safety, coverage, priority

    def score(self, candidate: Candidate, bootstrap: int = 500) -> CandidateScore:
        core = self._aggregate(candidate.evidence)
        rng = random.Random(self.seed + sum(ord(c) for c in candidate.name))
        samples = []
        for _ in range(bootstrap):
            draw = tuple(rng.choice(candidate.evidence) for _ in candidate.evidence)
            samples.append(self._aggregate(draw)[-1])
        samples.sort()
        lo = samples[int(0.05 * (len(samples)-1))]
        hi = samples[int(0.95 * (len(samples)-1))]
        leave_one_out = [self._aggregate(candidate.evidence[:i] + candidate.evidence[i+1:])[-1] for i in range(len(candidate.evidence))] if len(candidate.evidence) > 1 else [core[-1]]
        robustness = max(0.0, 1 - max(abs(value-core[-1]) for value in leave_one_out) / max(core[-1], 1e-9))
        return CandidateScore(candidate.name, *core, (lo, hi), robustness)

    def rank(self, candidates: list[Candidate]) -> list[CandidateScore]:
        return sorted((self.score(candidate) for candidate in candidates), key=lambda item: item.priority, reverse=True)
