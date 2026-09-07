# CreditPrice Agent

**State-dependent pricing of corporate loans under borrower risk, relationship history and bank balance-sheet constraints**

A credit model asks: *how risky is this borrower?*  
A pricing desk has a nastier question: *given the borrower, the relationship, today's funding curve, and the bank's current balance sheet, what price makes this loan worth doing?*

Those are not the same question. A bank can love a client and still dislike one more five-year asset in exactly the wrong sector. Balance sheets are sentimental only in PowerPoint.

## What this repository does

`CreditPrice Agent` is a reproducible research prototype for individualized corporate-loan pricing. It combines borrower risk (`PD`, `LGD`), relationship history, estimated price acceptance, market funding, and capital/liquidity/concentration pressure.

The central object is a **policy**:

`rate* = f(borrower, relationship, market, bank_state)`

The same borrower can therefore receive a different economically optimal price at two dates even if credit risk is unchanged.

## Reproducible experiment

The repository uses an explicit synthetic DGP rather than confidential bank data. That is less glamorous than leaking a credit book and considerably better for one's career.

```bash
pip install -e .[dev]
make experiment
make test
```

Reference run (`seed=42`, 30,000 applications):

- PD model AUC: **0.828**
- Historical mean quoted rate: **16.10%**
- Risk/demand-only optimized rate: **16.60%**
- State-dependent agent mean rate: **17.60%**
- Agent EV vs historical synthetic policy: **+70.3%**
- Agent EV vs risk/demand-only policy: **+7.9%**
- No-offer share: **0.0%** for the agent vs **0.0%** for the risk/demand-only policy

These are **simulation results**, not claims about a real bank. The DGP is visible in `src/credit_price_agent/simulation.py`, so the reader can inspect exactly where the rabbit entered the hat.

## Economic objective

For candidate rate `r`:

`EV(r) = P(accept|r,x,h) * [NII - EL - capital cost - state penalties + relationship value]`

The action space includes **no offer**. Sometimes the optimal price is not a price.

## Repository map

- `src/credit_price_agent/simulation.py` — structural synthetic DGP
- `src/credit_price_agent/models.py` — PD and acceptance models
- `src/credit_price_agent/economics.py` — economic-value function
- `src/credit_price_agent/optimizer.py` — constrained price search
- `scripts/run_experiment.py` — end-to-end experiment
- `tests/` — economic invariants
- `results/` — reference-run outputs
- `paper/` — SSRN-ready manuscript in PDF, DOCX and Markdown

## What this is not

This is not a production underwriting system, regulatory capital engine, or permission to discriminate between protected classes. Production use requires model-risk governance, fairness testing, calibration, policy constraints and legal review. Also meetings. Many meetings.

## Research contribution

The project treats loan pricing as a joint **borrower–relationship–bank-state** optimization problem. Borrower risk is necessary but insufficient because the marginal value of a loan depends on the lender's contemporaneous balance-sheet state.

## License

MIT for code. Please cite the accompanying working paper if you use the framework or experimental design.
