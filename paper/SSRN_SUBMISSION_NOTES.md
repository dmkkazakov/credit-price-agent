# SSRN submission notes

**Suggested title**  
CreditPrice Agent: State-Dependent Corporate Loan Pricing under Borrower Risk, Relationship History, and Dynamic Balance-Sheet Constraints

**Author**  
Dmitry Kazakov — NEIMARK University, Nizhny Novgorod, Russia

**Abstract**  
We study individualized corporate-loan pricing when the lender's own balance sheet is part of the decision state. The pricing policy conditions jointly on borrower fundamentals, relationship history, estimated price response, market funding and capital, liquidity and sector-concentration pressure. A transparent implementation separates risk estimation, demand estimation and constrained price search. A fully disclosed synthetic data-generating process contains 30,000 applications over 60 monthly states per run. In the seed-42 out-of-time experiment, the PD model achieves ROC AUC 0.828. Using structural acceptance probabilities and a common estimated PD, the state-dependent policy raises simulated economic value by 7.9% relative to a risk-and-demand optimizer and by 70.3% relative to the historical synthetic policy. A new seed-sensitivity experiment using five prespecified seeds (42-46), with 30,000 applications per seed, yields a mean uplift of 11.3% (range 7.9%-14.4%) relative to the risk-and-demand-only optimizer. This checks random-seed sensitivity under the same synthetic DGP, not robustness to alternative economic assumptions. These are simulation results, not estimated gains at a real institution. The contribution is a reproducible formulation of pricing as a borrower-relationship-bank-state decision with explicit limits on what the experiment establishes.

**Keywords**  
Corporate lending; loan pricing; risk-based pricing; price elasticity; balance-sheet optimization; machine learning; decision systems

**JEL**  
G21; G32; C61; C63

## Disclosure / positioning

- The empirical section uses synthetic data only.
- Results are reproducible from the repository with `seed=42`.
- Do not describe the simulation results as evidence about a real bank.
- The paper should be presented as a working paper / research prototype.
- Public source repository: https://github.com/dmkkazakov/credit-price-agent.
- Public paper record: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7427102.
- The reference run uses seed=42; the new documented seed-sensitivity series uses seeds 42-46. All five result sets are committed.
- Current academic affiliation: NEIMARK University, Nizhny Novgorod, Russia. Institutional affiliation does not imply university funding or endorsement.

## Suggested SSRN description

This working paper introduces a reproducible framework for state-dependent corporate-loan pricing. The model conditions jointly on borrower risk, relationship history, estimated price response, market funding and the lender's dynamic balance-sheet state. A fully disclosed synthetic DGP is used to evaluate counterfactual pricing policies without confidential bank data.

## Reproducibility checksum

Reference run: n=30000, seed=42, PD AUC=0.828,
agent vs risk/demand-only EV=+7.9%.

## Publication correction on 24 October 2026

The abstract in this submission-notes file previously retained obsolete values
(-1.4% and -109.7%) that disagreed with the manuscript and the saved metrics.
It is now copied from `paper/manuscript.md`: +7.9% versus the risk-and-demand
optimizer and +70.3% versus the deliberately imperfect historical synthetic
policy. This correction does not change the reference data or the computation.


## Revision on 30 October 2026

The SSRN record 7427102 must receive this revised abstract and the matching revised PDF. A local/GitHub update does not update SSRN. Replace the previously reported 9.8% five-seed summary with the measured 11.3% (7.9%-14.4%) series. Existing DOI and original written date remain unchanged.
