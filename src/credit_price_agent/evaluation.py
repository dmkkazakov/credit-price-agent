"""Structural acceptance for synthetic evaluation; zero denotes no offer."""
import numpy as np


def structural_pacc(rows, rates):
    rates = np.asarray(rates, dtype=float)
    if rates.shape != (len(rows),) or not np.all(np.isfinite(rates)) or np.any(rates < 0):
        raise ValueError('Expected one finite nonnegative rate per application')
    elasticity = (95 - 18 * rows.pd_true.to_numpy() + 8 * rows.previous_accept.to_numpy()
                  + 3 * np.minimum(rows.relationship_years.to_numpy(), 10) / 10)
    z = np.clip(elasticity * (rows.reservation_rate.to_numpy() - rates), -35, 35)
    return np.where(rates > 0, 1 / (1 + np.exp(-z)), 0.0)
