import contextlib
import io
from pathlib import Path
from types import SimpleNamespace
import threading
import unittest
import pandas as pd
from helpers import functions_from

APP = Path(__file__).resolve().parents[1] / "New_Project"


class MarketRegressions(unittest.TestCase):
    def technicals(self, closes):
        hist = pd.DataFrame({"Close": closes, "High": closes, "Low": closes, "Volume": [100] * len(closes)})
        stock = SimpleNamespace(history=lambda **kw: hist.copy(), info={})
        ns = functions_from(APP / "mcp_server/finance_api.py", yf=SimpleNamespace(Ticker=lambda ticker: stock), pd=pd)
        return ns["get_technical_data"]("TEST")

    def test_rsi_gain_loss_flat_and_mixed(self):
        series = [(list(range(100, 160)), 100), (list(range(160, 100, -1)), 0), ([100] * 60, 50), ([100, 101] * 30, 50)]
        for prices, expected in series:
            with self.subTest(expected=expected):
                result = self.technicals(prices)
                self.assertEqual(result["rsi_14"], expected)
                self.assertTrue(0 <= result["rsi_14"] <= 100)

    def test_empty_prices_return_consistent_error(self):
        self.assertIn("error", self.technicals([]))

    def test_invalid_ticker_stops_before_analysts(self):
        ns = functions_from(APP / "graph/workflow.py",
            get_fundamental_data=lambda ticker: {"error": "not found"},
            get_technical_data=lambda ticker: self.fail("Must not fetch more data after rejection"))
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            ns["data_ingestion_node"]({"ticker": "INVALID"})

    def test_rejection_terminates_checkpoint(self):
        updates = []
        fake = SimpleNamespace(get_state=lambda config: SimpleNamespace(next=("portfolio_manager",)),
            update_state=lambda *args, **kw: updates.append(kw),
            stream=lambda *args, **kw: self.fail("Rejected research must not invoke the model"))
        # Decorators are supplied by a tiny no-op API registration stub.
        app = SimpleNamespace(get=lambda *a: lambda f: f, post=lambda *a: lambda f: f)
        ns = functions_from(APP / "api/routes.py", app=app, graph=fake, graph_lock=threading.Lock())
        result = ns["approve_research"](SimpleNamespace(thread_id="session", action="reject"))
        self.assertEqual(updates, [{"as_node": "portfolio_manager"}])
        self.assertIn("rejected", result["message"])


if __name__ == "__main__": unittest.main()
