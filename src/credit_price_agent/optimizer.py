from __future__ import annotations
import numpy as np
import pandas as pd
from .models import predict_acceptance_at_rate
from .economics import expected_value

def optimize_rates(rows, pd_hat, accept_model, state_dependent=True,
                   grid=None, min_spread=0.005):
    if grid is None:
        grid = np.arange(0.06, 0.301, 0.0025)
    best_rate = np.zeros(len(rows))
    best_ev = np.zeros(len(rows))  # no-offer action has EV=0
    best_pa = np.zeros(len(rows))

    for rate in grid:
        pacc = predict_acceptance_at_rate(accept_model, rows, rate)
        floor = rows["market_rate"].to_numpy() + rows["funding_spread"].to_numpy() + min_spread
        feasible = rate >= floor
        ev = expected_value(
            rate=rate, amount=rows["amount"].to_numpy(), tenor=rows["tenor_years"].to_numpy(),
            pd=pd_hat, lgd=rows["lgd_true"].to_numpy(), p_accept=pacc,
            market_rate=rows["market_rate"].to_numpy(), funding_spread=rows["funding_spread"].to_numpy(),
            capital_pressure=rows["capital_pressure"].to_numpy(),
            liquidity_pressure=rows["liquidity_pressure"].to_numpy(),
            sector_pressure=rows["sector_pressure"].to_numpy(),
            relationship_years=rows["relationship_years"].to_numpy(),
            state_dependent=state_dependent
        )
        ev = np.where(feasible, ev, -np.inf)
        take = ev > best_ev
        best_ev[take] = ev[take]
        best_rate[take] = rate
        best_pa[take] = pacc[take]
    return pd.DataFrame({"recommended_rate":best_rate, "expected_value":best_ev, "p_accept":best_pa}, index=rows.index)
