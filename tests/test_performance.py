import pytest
from io import StringIO
from unittest.mock import MagicMock
import re

from src.backtesting.backtester import Backtester
from src.backtesting.portfolio import Portfolio
from src.backtesting.trade import Trade
from datetime import datetime

@pytest.fixture
def mock_backtester():
    # Create a backtester instance with a mock strategy
    class MockStrategy:
        def update_price(self, future_price: float) -> None:
            pass
        def generate_signal(self) -> str:
            return "hold"
    
    backtester = Backtester(strategy=MockStrategy(), initial_cash=100000.0)
    # Manually set some trades in the portfolio to test performance calculation
    # Suppose we have 5 trades: 2 winners, 3 losers
    # Trades with their realized PnL values:
    # Trade 1: +10.0
    # Trade 2: +5.0
    # Trade 3: -2.0
    # Trade 4: -4.0
    # Trade 5: -9.0
    
    portfolio = backtester._portfolio
    portfolio.completed_trades = [
        _make_trade(pnl=10.0),
        _make_trade(pnl=5.0),
        _make_trade(pnl=-2.0),
        _make_trade(pnl=-4.0),
        _make_trade(pnl=-9.0),
    ]
    # Set a final index price for final_equity calculation
    backtester._current_index_price = 6080.0
    
    return backtester

def _make_trade(pnl: float) -> Trade:
    # Create a closed trade with the given PnL for testing
    trade = Trade(direction="long", open_time=datetime(2024,1,1,9,30,0), open_price=6000.0)
    trade.close_trade(close_time=datetime(2024,1,1,9,40,0), close_price=6000.0) 
    # Override realized_pnl directly
    trade.realized_pnl = pnl
    return trade


def test_print_performance(mock_backtester, capsys):
    # Run print_performance
    mock_backtester.print_performance()
    
    # Capture the printed output
    captured = capsys.readouterr()
    out = captured.out.strip()

    # Check that all required metrics are printed
    assert "Number of Trades: 5" in out
    assert "Winners: 2" in out
    assert "Losers: 3" in out
    assert "Average PnL: 0.00" in out

    # Extract Geometric Mean PnL per Trade using regex
    match = re.search(r"Geometric Mean PnL per Trade: (-?\d+\.\d+e?-?\d*)", out)
    assert match, "Geometric Mean PnL per Trade not found in output"
    
    # Convert the extracted value to a float
    geometric_mean_pnl = float(match.group(1))
    
    # Check if the geometric mean is close to 0 with a tolerance
    assert abs(geometric_mean_pnl) < 1e-6, f"Expected Geometric Mean ~0, but got {geometric_mean_pnl}"
    
    # Check Sharpe Ratio
    assert "Sharpe Ratio: 0.0000" in out
    
    # Check Final Portfolio Value
    assert "Final Portfolio Value: 100000.00" in out
