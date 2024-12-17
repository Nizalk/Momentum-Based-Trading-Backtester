import pytest
from datetime import datetime
from src.backtesting.portfolio import Portfolio
from src.backtesting.trade import Trade

def test_open_long_position():
    """Test opening a long position starting from 2024/12/03."""
    portfolio = Portfolio()
    portfolio.set_current_time(datetime(2024, 12, 3, 9, 30, 0)) 
    success = portfolio.open_position(direction="long", price=5000.0)

    assert success, "Opening a long position should succeed"
    assert portfolio.cash == 100000.0 - 2.0, "Cash should be reduced by commission"
    assert portfolio.open_trade is not None, "There should now be an open trade"
    assert portfolio.open_trade.direction == "long", "The trade direction should be long"

def test_close_long_position():
    """Test closing a long position with correct PnL and commission handling."""
    portfolio = Portfolio()
    portfolio.set_current_time(datetime(2024, 12, 3, 9, 30, 0))
    
    # Open a long position
    portfolio.open_position(direction="long", price=5000.0)
    assert portfolio.cash == 100000.0 - 2.0, "Cash should deduct commission when opening position"
    
    # Close the long position
    portfolio.set_current_time(datetime(2024, 12, 3, 10, 0, 0))
    portfolio.close_position(price=5100.0)
    
    # Assertions
    assert portfolio.open_trade is None, "Open trade should be None after closing position"
    assert len(portfolio.completed_trades) == 1, "Trade should be added to completed trades"
    assert portfolio.cash == 100096.0, "Final cash should include realized PnL and deducted commissions"


def test_close_short_position():
    """Test closing a short position."""
    portfolio = Portfolio()
    portfolio.set_current_time(datetime(2024, 12, 3, 9, 30, 0))
    portfolio.open_position(direction="short", price=5000.0)
    portfolio.set_current_time(datetime(2024, 12, 3, 10, 0, 0))
    portfolio.close_position(price=4900.0)

    margin_return = 0.5 * 5000.0
    assert portfolio.open_trade is None, "No open trades should exist after closing"
    assert len(portfolio.completed_trades) == 1, "Closed trade should be added to completed trades"
    assert portfolio.cash == 100000.0 - 2.0 - 2.0 - margin_return + margin_return + 100.0, "Cash should reflect PnL, commissions, and margin return"

def test_unrealized_pnl():
    """Test unrealized PnL calculation for long and short positions."""
    portfolio = Portfolio()
    portfolio.set_current_time(datetime(2024, 12, 3, 9, 30, 0))
    portfolio.open_position(direction="long", price=5000.0)

    # Long position with price increase
    assert portfolio.get_unrealized_pnl(5100.0) == 100.0, "Unrealized PnL should be correct for long trade"

    portfolio.close_position(price=5100.0)
    portfolio.open_position(direction="short", price=5000.0)

    # Short position with price decrease
    assert portfolio.get_unrealized_pnl(4900.0) == 100.0, "Unrealized PnL should be correct for short trade"

def test_total_equity():
    """Test total equity calculation."""
    portfolio = Portfolio()
    portfolio.set_current_time(datetime(2024, 12, 3, 9, 30, 0))
    portfolio.open_position(direction="long", price=5000.0)

    unrealized_pnl = 100.0
    expected_equity = 100000.0 - 2.0 + unrealized_pnl
    assert portfolio.total_equity(current_price=5100.0) == expected_equity, "Total equity should include cash and unrealized PnL"
