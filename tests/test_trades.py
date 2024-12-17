import pytest
from datetime import datetime
from src.backtesting.trade import Trade

def test_trade_initialization():
    """Test initialization of a Trade object."""
    trade = Trade(
        direction="long",
        open_time=datetime(2024, 12, 3, 9, 30, 0),
        open_price=5000.0,
        size=1
    )
    
    assert trade.direction == "long", "Direction should be initialized correctly"
    assert trade.open_time == datetime(2024, 12, 3, 9, 30, 0), "Open time mismatch"
    assert trade.open_price == 5000.0, "Open price mismatch"
    assert trade.size == 1, "Trade size mismatch"
    assert trade.close_time is None, "Close time should initialize as None"
    assert trade.close_price is None, "Close price should initialize as None"
    assert trade.realized_pnl is None, "PNL should initialize as None"

def test_close_trade_long():
    """Test closing a long trade and calculating realized PnL."""
    trade = Trade(
        direction="long",
        open_time=datetime(2024, 12, 3, 9, 30, 0),
        open_price=5000.0,
        size=1
    )
    trade.close_trade(close_time=datetime(2024, 12, 3, 10, 0, 0), close_price=5100.0)
    
    assert trade.close_time == datetime(2024, 12, 3, 10, 0, 0), "Close time mismatch"
    assert trade.close_price == 5100.0, "Close price mismatch"
    assert trade.realized_pnl == 100.0, "Realized PnL should be correct for long trade"

def test_close_trade_short():
    """Test closing a short trade and calculating realized PnL."""
    trade = Trade(
        direction="short",
        open_time=datetime(2024, 12, 3, 9, 30, 0),
        open_price=5000.0,
        size=1
    )
    trade.close_trade(close_time=datetime(2024, 12, 3, 10, 0, 0), close_price=4900.0)
    
    assert trade.close_time == datetime(2024, 12, 3, 10, 0, 0), "Close time mismatch"
    assert trade.close_price == 4900.0, "Close price mismatch"
    assert trade.realized_pnl == 100.0, "Realized PnL should be correct for short trade"

def test_trade_zero_size():
    """Test behavior of a trade with zero size."""
    trade = Trade(
        direction="long",
        open_time=datetime(2024, 12, 3, 9, 30, 0),
        open_price=5000.0,
        size=0
    )
    trade.close_trade(close_time=datetime(2024, 12, 3, 10, 0, 0), close_price=5100.0)
    
    assert trade.realized_pnl == 0.0, "Realized PnL should be 0 for zero-size trade"

def test_close_trade_no_price_change():
    """Test closing a trade with no price change."""
    trade = Trade(
        direction="long",
        open_time=datetime(2024, 12, 3, 9, 30, 0),
        open_price=5000.0,
        size=1
    )
    trade.close_trade(close_time=datetime(2024, 12, 3, 10, 0, 0), close_price=5000.0)
    
    assert trade.realized_pnl == 0.0, "Realized PnL should be 0 when there is no price change"
