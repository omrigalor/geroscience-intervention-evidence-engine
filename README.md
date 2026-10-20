# Geroscience Intervention Evidence Engine

An uncertainty-aware research system for comparing longevity-intervention hypotheses without confusing a promising mechanism with proven human benefit. The engine combines study design, species translation, replication, uncertainty, safety, hallmark coverage, and source diversity, then reports both a priority score and how fragile it is to any one evidence source.

## What it calculates

- reliability-weighted evidence strength;
- species-to-human translation weight;
- safety and twelve-hallmark coverage;
- a composite preclinical research-priority score;
- a seeded bootstrap 90% uncertainty interval;
- leave-one-source-out robustness;
- a ranked candidate list with every input inspectable.

The included records are deliberately illustrative. They show how the framework treats mTOR evidence and partial epigenetic reprogramming; they are not a clinical recommendation, a complete evidence review, or a forecast that an intervention will extend human lifespan.

## Why it is distinct

A high-effect mouse study should not automatically outrank smaller but replicated human evidence, and a single spectacular source should not look robust. The model therefore separates effect, evidence reliability, translation, safety, breadth, and source dependence. “Predictive power” belongs in a held-out validation result; the repository provides the scoring and robustness scaffold needed to test it once a curated outcome dataset is supplied.

## Run

```bash
python -m pip install -e . pytest
python demo.py
pytest -q
```

## Research basis

- Takahashi & Yamanaka (2006), *Induction of pluripotent stem cells from mouse embryonic and adult fibroblast cultures by defined factors*, Cell. DOI: 10.1016/j.cell.2006.07.024.
- Harrison et al. (2009), *Rapamycin fed late in life extends lifespan in genetically heterogeneous mice*, Nature. DOI: 10.1038/nature08221.
- Lu et al. (2020), *Reprogramming to recover youthful epigenetic information and restore vision*, Nature. DOI: 10.1038/s41586-020-2975-4.
- López-Otín et al. (2023), *Hallmarks of aging: An expanding universe*, Cell. DOI: 10.1016/j.cell.2022.11.001.
- National Institute on Aging, Interventions Testing Program: multi-site lifespan testing in genetically heterogeneous UM-HET3 mice.
- Barardo et al. (2017), *The DrugAge database of aging-related drugs*, Aging Cell. DOI: 10.1111/acel.12585.

## Validation boundary

This is a research-prioritization prototype, not medical advice, drug-discovery validation, or evidence that any intervention slows human aging. The weights are explicit normative assumptions. A serious predictive claim requires preregistered endpoints, a curated longitudinal dataset, held-out evaluation, calibration checks, and prospective replication.
