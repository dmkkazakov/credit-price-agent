import unittest
import numpy as np
from credit_price_agent.simulation import generate_portfolio
from credit_price_agent.evaluation import structural_pacc
from credit_price_agent.economics import expected_value
from credit_price_agent.optimizer import optimize_rates


class ConstantDemand:
    def predict_proba(self, rows):
        return np.tile([0.3, 0.7], (len(rows), 1))


class NoOfferTests(unittest.TestCase):
    def setUp(self):
        self.rows = generate_portfolio(n=20, seed=42)

    def test_no_offer_zero_acceptance_and_ev(self):
        p = structural_pacc(self.rows, np.zeros(len(self.rows)))
        np.testing.assert_array_equal(p, 0)
        ev = expected_value(0, self.rows.amount.to_numpy(), 3, .02, .35, p, .09, .015)
        np.testing.assert_array_equal(ev, 0)

    def test_infeasible_optimizer_grid(self):
        result = optimize_rates(self.rows, np.full(len(self.rows), .02), ConstantDemand(), grid=[.001])
        np.testing.assert_array_equal(result.recommended_rate, 0)
        np.testing.assert_array_equal(structural_pacc(self.rows, result.recommended_rate.to_numpy()), 0)

    def test_mixed_offers_preserve_positive_rate_probabilities(self):
        rates = np.full(len(self.rows), .18)
        expected = structural_pacc(self.rows, rates)
        rates[::2] = 0
        got = structural_pacc(self.rows, rates)
        np.testing.assert_array_equal(got[::2], 0)
        np.testing.assert_allclose(got[1::2], expected[1::2])

    def test_invalid_rate_rejected(self):
        for value in [-1, np.nan, np.inf]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                structural_pacc(self.rows, np.full(len(self.rows), value))
        with self.assertRaises(ValueError):
            structural_pacc(self.rows, [0.18])


if __name__ == '__main__':
    unittest.main()
