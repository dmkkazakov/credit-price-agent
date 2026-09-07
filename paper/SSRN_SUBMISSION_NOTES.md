# SSRN submission notes

**Suggested title**  
CreditPrice Agent: State-Dependent Corporate Loan Pricing under Borrower Risk, Relationship History, and Dynamic Balance-Sheet Constraints

**Author**  
Dmitry Kazakov — Independent Researcher

**Abstract**  
Loan pricing is often modeled as a borrower-level problem: estimate credit risk, add funding and capital costs, and choose a margin. This paper studies a different formulation. The economically relevant price of a corporate loan depends not only on the borrower but also on the lender's contemporaneous state. We introduce CreditPrice Agent, a transparent research framework in which the pricing policy conditions jointly on borrower risk, relationship history, price acceptance, market funding, and dynamic balance-sheet pressure. A structural synthetic data-generating process makes the counterfactual pricing problem observable and reproducible without using confidential bank data. In a reference simulation of 30,000 applications, the state-dependent policy changes quoted prices relative to a risk-and-demand-only optimizer and increases simulated total economic value by -1.4% under the known data-generating process. Relative to the historical synthetic policy, the improvement is -109.7%. These figures are simulation results, not empirical claims about any institution. The main contribution is conceptual and operational: corporate loan pricing is represented as a borrower-relationship-bank-state decision rather than a static markup over expected loss.

**Keywords**  
Corporate lending; loan pricing; risk-based pricing; price elasticity; balance-sheet optimization; machine learning; decision systems

**JEL**  
G21; G32; C61; C63

## Disclosure / positioning

- The empirical section uses synthetic data only.
- Results are reproducible from the repository with `seed=42`.
- Do not describe the simulation results as evidence about a real bank.
- The paper should be presented as a working paper / research prototype.
- Before public upload, add the final public GitHub repository URL to the manuscript and CITATION.cff.
- Verify any employer/affiliation and conflict-of-interest wording before submission.

## Suggested SSRN description

This working paper introduces a reproducible framework for state-dependent corporate-loan pricing. The model conditions jointly on borrower risk, relationship history, estimated price response, market funding and the lender's dynamic balance-sheet state. A fully disclosed synthetic DGP is used to evaluate counterfactual pricing policies without confidential bank data.

## Reproducibility checksum

Reference run: n=30000, seed=42, PD AUC=0.828,
agent vs risk/demand-only EV=+7.9%.
