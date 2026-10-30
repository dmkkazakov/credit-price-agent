import unittest
import numpy as np
from credit_price_agent.economics import expected_value

class EconomicsTests(unittest.TestCase):
    def test_balance_pressure_reduces_value(self):
        low = expected_value(.14, 10, 3, .02, .35, .7, .09, .015, 0,0,0,5, True)
        high = expected_value(.14, 10, 3, .02, .35, .7, .09, .015, 1,1,1,5, True)
        assert high < low

    def test_zero_acceptance_zero_value(self):
        v = expected_value(.14, 10, 3, .02, .35, 0, .09, .015)
        assert abs(float(v)) < 1e-12

