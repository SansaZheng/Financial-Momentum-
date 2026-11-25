import unittest
import numpy as np

from research.metrics import portfolio_returns, sharpe
from research.synthetic_mechanisms import make_panel, causal_momentum, gated_signal


class ResearchContracts(unittest.TestCase):
    def test_costs_are_nonpositive_and_turnover_is_causal(self):
        r = np.ones((3, 2)) * 0.01
        w = np.array([[0.5, 0.5], [0.5, 0.5], [0.0, 0.0]])
        gross, net, turnover = portfolio_returns(w, r, cost_bps=10)
        np.testing.assert_allclose(turnover, [1.0, 0.0, 1.0])
        self.assertTrue(np.all(net <= gross))

    def test_future_mutation_does_not_change_prefix_signal(self):
        r, score, _ = make_panel("trend_flip", seed=3, t=200)
        w1 = causal_momentum(r)
        r2 = r.copy(); r2[150:] = 99.0
        w2 = causal_momentum(r2)
        np.testing.assert_array_equal(w1[:150], w2[:150])

    def test_mechanism_labels_are_explicit(self):
        for kind in ("trend_flip", "variance_only", "no_change"):
            r, score, cp = make_panel(kind, seed=1, t=100)
            self.assertEqual(r.shape, (100, 4)); self.assertEqual(cp, 50)
            self.assertEqual(gated_signal(r, score, 0.0).shape, r.shape)

    def test_constant_sharpe_is_nan(self):
        self.assertTrue(np.isnan(sharpe(np.ones(5))))


if __name__ == "__main__":
    unittest.main()
