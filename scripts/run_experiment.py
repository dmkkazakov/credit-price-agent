from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from credit_price_agent.simulation import generate_portfolio
from credit_price_agent.models import fit_pd_model, fit_acceptance_model, RISK_NUM, CAT
from credit_price_agent.optimizer import optimize_rates
from credit_price_agent.economics import expected_value

ROOT = Path(__file__).resolve().parents[1]
df = generate_portfolio(n=30000, seed=42)
train = df[df.month < 48].copy()
test = df[df.month >= 48].copy()

pd_model = fit_pd_model(train)
acc_model = fit_acceptance_model(train)
pd_hat = pd_model.predict_proba(test[RISK_NUM+CAT])[:,1]
auc = roc_auc_score(test.default, pd_hat)

agent = optimize_rates(test, pd_hat, acc_model, state_dependent=True)
risk_only = optimize_rates(test, pd_hat, acc_model, state_dependent=False)

# Historical-policy EV evaluated using structural acceptance probability approximation
def structural_pacc(rows, rate):
    elasticity = 95 - 18*rows.pd_true.to_numpy() + 8*rows.previous_accept.to_numpy() + 3*np.minimum(rows.relationship_years.to_numpy(),10)/10
    z = np.clip(elasticity*(rows.reservation_rate.to_numpy()-rate), -35, 35)
    return 1/(1+np.exp(-z))

hist_pa = structural_pacc(test, test.offered_rate.to_numpy())
hist_ev = expected_value(
    test.offered_rate.to_numpy(), test.amount.to_numpy(), test.tenor_years.to_numpy(),
    pd_hat, test.lgd_true.to_numpy(), hist_pa,
    test.market_rate.to_numpy(), test.funding_spread.to_numpy(),
    test.capital_pressure.to_numpy(), test.liquidity_pressure.to_numpy(), test.sector_pressure.to_numpy(),
    test.relationship_years.to_numpy(), True
)
# Evaluate learned policies against known synthetic DGP (not the fitted demand model).
agent_pa_true = structural_pacc(test, agent.recommended_rate.to_numpy())
agent_ev_true = expected_value(
    agent.recommended_rate.to_numpy(), test.amount.to_numpy(), test.tenor_years.to_numpy(),
    pd_hat, test.lgd_true.to_numpy(), agent_pa_true,
    test.market_rate.to_numpy(), test.funding_spread.to_numpy(),
    test.capital_pressure.to_numpy(), test.liquidity_pressure.to_numpy(), test.sector_pressure.to_numpy(),
    test.relationship_years.to_numpy(), True
)
risk_pa_true = structural_pacc(test, risk_only.recommended_rate.to_numpy())
risk_ev_true = expected_value(
    risk_only.recommended_rate.to_numpy(), test.amount.to_numpy(), test.tenor_years.to_numpy(),
    pd_hat, test.lgd_true.to_numpy(), risk_pa_true,
    test.market_rate.to_numpy(), test.funding_spread.to_numpy(),
    test.capital_pressure.to_numpy(), test.liquidity_pressure.to_numpy(), test.sector_pressure.to_numpy(),
    test.relationship_years.to_numpy(), True
)

metrics = {
    "n_total": int(len(df)), "n_train": int(len(train)), "n_test": int(len(test)),
    "pd_auc": float(auc),
    "historical_mean_rate": float(test.offered_rate.mean()),
    "risk_only_mean_rate": float(risk_only.recommended_rate.mean()),
    "agent_mean_rate": float(agent.recommended_rate.mean()),
    "historical_total_ev": float(np.sum(hist_ev)),
    "risk_only_total_ev": float(np.sum(risk_ev_true)),
    "agent_total_ev": float(np.sum(agent_ev_true)),
    "agent_vs_historical_ev_pct": float((np.sum(agent_ev_true)/np.sum(hist_ev)-1)*100),
    "agent_vs_risk_only_ev_pct": float((np.sum(agent_ev_true)/np.sum(risk_ev_true)-1)*100),
    "historical_acceptance": float(hist_pa.mean()),
    "agent_acceptance": float(agent_pa_true.mean()),
    "risk_only_acceptance": float(risk_pa_true.mean()),
}
(ROOT/"results"/"metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
out = test[["month","industry","pd_true","lgd_true","amount","relationship_years","capital_pressure","liquidity_pressure","sector_pressure","offered_rate"]].copy()
out["pd_hat"] = pd_hat
out["risk_only_rate"] = risk_only.recommended_rate
out["agent_rate"] = agent.recommended_rate
out["agent_ev"] = agent_ev_true
out.to_csv(ROOT/"results"/"policy_results.csv", index=False)
df.head(1000).to_csv(ROOT/"data"/"sample"/"synthetic_loan_applications.csv", index=False)
print(json.dumps(metrics, indent=2))
