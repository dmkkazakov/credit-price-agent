from __future__ import annotations
import numpy as np

def expected_value(rate, amount, tenor, pd, lgd, p_accept, market_rate, funding_spread,
                   capital_pressure=0.0, liquidity_pressure=0.0, sector_pressure=0.0,
                   relationship_years=0.0, state_dependent=True):
    """
    Simplified economic value in synthetic currency units.
    The balance-sheet penalties are deliberately transparent rather than hidden in a black box.
    """
    funding = market_rate + funding_spread
    net_spread = rate - funding
    nii = amount * tenor * net_spread
    expected_loss = amount * pd * lgd
    capital_cost = amount * (0.012 + 0.030*pd) * tenor

    state_penalty = 0.0
    if state_dependent:
        state_penalty = amount * (
            0.0250*capital_pressure +
            0.0200*liquidity_pressure +
            0.0180*sector_pressure
        )
    relationship_value = amount * 0.0008 * np.minimum(relationship_years, 10.0)
    return p_accept * (nii - expected_loss - capital_cost - state_penalty + relationship_value)
