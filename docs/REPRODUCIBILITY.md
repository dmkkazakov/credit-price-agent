# Reproduction and correction record

Revision: 30 October 2026. Software: 0.3.1.

## What was verified

Five full experiments were run with seeds **42, 43, 44, 45, 46**, with 30,000 synthetic applications per seed. Each run retrains the models and evaluates both policies on its own held-out split. All five runs are retained, including the reference seed 42; no seed was excluded.

| Seed | Agent EV uplift over risk/demand policy |
| --- | ---: |
| 42 | 7.9224% |
| 43 | 11.5597% |
| 44 | 12.1187% |
| 45 | 10.4376% |
| 46 | 14.4199% |
| Arithmetic mean | **11.2917%** |

The range is **7.9224–14.4199%**. This is random-seed sensitivity under one fixed synthetic data-generating process. It is not a confidence interval, parameter-robustness study, observed bank return or production validation. The unweighted mean of the five percentage uplifts is reported, rather than the ratio of pooled economic values.

The reference seed-42 result remains **7.9%** against the optimized risk/demand comparator and **70.3%** against the deliberately imperfect historical synthetic policy. These comparisons answer different questions.

## Corrections

- The earlier SSRN abstract reported a five-seed mean of 9.8% and a range of 7.5–12.2%, but corresponding per-seed artifacts were not available in the repository. The newly recorded experiment supports 11.3% and 7.9–14.4%. It does not reconstruct or validate the earlier figures.
- The evaluator now treats rate zero as **no offer**: acceptance and economic value are zero. Previously, structural acceptance could interpret that sentinel as an offered zero-interest loan. All five recorded runs have a zero no-offer share, so this correction does not change their reported aggregate result; dedicated boundary tests cover the case.
- Evaluation uses structural acceptance probabilities and a shared **estimated PD**. It is not a fully structural counterfactual-default evaluation. This limitation is now explicit in the manuscript and README.
- Markdown, DOCX, PDF, citation metadata and submission fields have been aligned. Updating repository files does not replace the abstract or PDF hosted by SSRN; that requires an authenticated author revision.

## Reproduce

Recorded environment: Python 3.12.14, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0.

```bash
python -m pip install -r requirements-reproduction.txt
python -m pip install -e . --no-deps
python -m unittest discover -s tests -v
python scripts/run_experiment.py --seed 42
python scripts/run_seed_sensitivity.py
```

Six unit tests cover the existing economic invariants, infeasible-grid no-offer behavior, mixed offer/no-offer evaluation, and invalid rate inputs. They do not establish model validity on real borrowers.

[`summary.json`](../results/seed_sensitivity/summary.json) retains exact metrics and package versions. Each `seed_*` directory contains metrics, policy-level outputs and a synthetic-data sample. CSV files use lossless gzip compression (`.csv.gz`); pandas reads them directly, or decompress them with `gzip -dk`. [`manifest.json`](../results/seed_sensitivity/manifest.json) records SHA-256 hashes of the experiment source and retained outputs. The main `results/metrics.json` is the seed-42 reference.
