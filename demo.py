from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))
from geroscience_evidence import Candidate, Evidence, EvidenceEngine


def row(source, species, design, effect, uncertainty, replication, safety, *hallmarks):
    return Evidence(source, species, design, effect, uncertainty, replication, safety, hallmarks)


candidates = [
    Candidate("mTOR modulation", (
        row("ITP-2009", "mouse", "multisite", .78, .16, .95, .58, "nutrient-sensing", "autophagy"),
        row("ITP-followup", "mouse", "multisite", .72, .18, .92, .60, "nutrient-sensing"),
        row("human-feasibility", "human", "randomized", .28, .42, .48, .50, "immune-function"),
    )),
    Candidate("partial epigenetic reprogramming", (
        row("mouse-retina", "mouse", "single_site", .66, .28, .55, .38, "epigenetic-alteration", "stem-cell-exhaustion"),
        row("cell-reprogramming", "cell", "single_site", .74, .22, .72, .30, "epigenetic-alteration"),
    )),
]

for result in EvidenceEngine().rank(candidates):
    print(f"{result.name:36} priority={result.priority:.3f}  90% interval={result.interval_90}  robustness={result.robustness:.2f}")
