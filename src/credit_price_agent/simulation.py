from __future__ import annotations
import numpy as np
import pandas as pd

INDUSTRIES = np.array(["manufacturing","energy","retail","transport","telecom","services"])

def sigmoid(x):
    x = np.clip(x, -35, 35)
    return 1.0 / (1.0 + np.exp(-x))

def generate_portfolio(n=30000, seed=42):
    """Generate synthetic corporate-loan applications from an explicit structural DGP."""
    rng = np.random.default_rng(seed)
    month = rng.integers(0, 60, n)
    industry_idx = rng.integers(0, len(INDUSTRIES), n)
    industry = INDUSTRIES[industry_idx]

    log_revenue = rng.normal(4.0, 0.85, n)
    revenue = np.exp(log_revenue)
    ebitda_margin = np.clip(rng.normal(0.18, 0.08, n), 0.02, 0.55)
    leverage = np.clip(rng.gamma(2.0, 0.85, n), 0.05, 7.0)
    interest_cover = np.clip(7.0 / (1.0 + leverage) + rng.normal(0, .8, n), .25, 12)
    relationship_years = np.clip(rng.gamma(2.2, 2.0, n), 0, 20)
    repayment_score = np.clip(rng.beta(8, 2, n), 0.05, 1.0)
    previous_accept = np.clip(rng.beta(5, 2, n), .05, .99)

    # Market/bank state evolves over time.
    market_rate = 0.085 + 0.018*np.sin(month/7.0) + 0.00045*month + rng.normal(0,.004,n)
    funding_spread = 0.012 + 0.007*np.sin(month/5.5 + 1) + rng.normal(0,.0025,n)
    liquidity_pressure = np.clip(0.45 + 0.22*np.sin(month/6.0) + rng.normal(0,.12,n), 0, 1)
    capital_pressure = np.clip(0.40 + 0.20*np.cos(month/8.0) + rng.normal(0,.11,n), 0, 1)
    sector_pressure = np.clip(0.25 + 0.08*industry_idx + rng.normal(0,.12,n), 0, 1)

    pd_true = sigmoid(
        -5.25 + .58*leverage - .38*interest_cover - .65*repayment_score
        - .045*relationship_years + .12*(industry_idx==2) + rng.normal(0,.22,n)
    )
    lgd_true = np.clip(.22 + .055*leverage + .10*(industry_idx==2) + rng.normal(0,.06,n), .08, .75)

    amount = np.exp(rng.normal(2.0, .9, n))
    amount = np.clip(amount, .2, 80.0)  # synthetic currency units, millions
    tenor_years = rng.choice([1,2,3,5,7], n, p=[.18,.22,.28,.22,.10])

    # Latent willingness-to-pay / reservation rate.
    relationship_discount = .0009*np.minimum(relationship_years, 10)
    risk_component = .65*pd_true*lgd_true
    reservation_rate = (
        market_rate + funding_spread + .032 + risk_component
        - relationship_discount + .006*(1-repayment_score)
        + rng.normal(0,.008,n)
    )

    # Historical bank policy: imperfect, mostly risk-based.
    offered_rate = (
        market_rate + funding_spread + .026 + .72*pd_true*lgd_true
        + .004*capital_pressure + rng.normal(0,.006,n)
    )
    offered_rate = np.clip(offered_rate, .055, .32)

    elasticity = 95 - 18*pd_true + 8*previous_accept + 3*np.minimum(relationship_years,10)/10
    p_accept = sigmoid(elasticity*(reservation_rate - offered_rate))
    accepted = rng.binomial(1, p_accept)

    default = rng.binomial(1, np.clip(pd_true*(1 + .12*(offered_rate-reservation_rate>0)), 0, .45))
    return pd.DataFrame({
        "month":month, "industry":industry, "industry_idx":industry_idx,
        "revenue":revenue, "ebitda_margin":ebitda_margin, "leverage":leverage,
        "interest_cover":interest_cover, "relationship_years":relationship_years,
        "repayment_score":repayment_score, "previous_accept":previous_accept,
        "market_rate":market_rate, "funding_spread":funding_spread,
        "liquidity_pressure":liquidity_pressure, "capital_pressure":capital_pressure,
        "sector_pressure":sector_pressure, "pd_true":pd_true, "lgd_true":lgd_true,
        "amount":amount, "tenor_years":tenor_years, "reservation_rate":reservation_rate,
        "offered_rate":offered_rate, "accepted":accepted, "default":default
    })
