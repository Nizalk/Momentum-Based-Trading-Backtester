from src.backtesting.strategies.momentumstrategy import MomentumStrategy
import pytest

def test_momentum_strategy_signals():
    """Test the signal generation for the momentum strategy."""
    strategy = MomentumStrategy(threshold=0.0005)

    # Step 1: Fill less than 10 prices - should always return "hold"
    for price in [100.0, 100.1, 100.2, 100.3, 100.4]:
        strategy.update_price(price)
        assert strategy.generate_signal() == "hold", "Signal should be 'hold' with insufficient data"

    # Step 2: Provide 10 prices to allow momentum computation
    prices = [100.0, 100.1, 100.2, 100.3, 100.4, 100.6, 100.7, 100.8, 100.9, 101.0]
    for price in prices:
        strategy.update_price(price)

    # Momentum = (X_n - X_n-1) / X_n where:
    # - X_n: average of [100.6, 100.7, 100.8, 100.9, 101.0] = 100.8
    # - X_n-1: average of [100.0, 100.1, 100.2, 100.3, 100.4] = 100.2
    # Momentum = (100.8 - 100.2) / 100.8 ≈ 0.00595 (> threshold)
    assert strategy.generate_signal() == "buy", "Signal should be 'buy' when momentum > threshold"

    # Step 3: Decrease prices to trigger "sell"
    prices = [100.4, 100.3, 100.2, 100.1, 100.0, 99.8, 99.7, 99.6, 99.5, 99.4]
    for price in prices:
        strategy.update_price(price)

    # Momentum = (X_n - X_n-1) / X_n where:
    # - X_n: average of [99.8, 99.7, 99.6, 99.5, 99.4] = 99.6
    # - X_n-1: average of [100.4, 100.3, 100.2, 100.1, 100.0] = 100.2
    # Momentum = (99.6 - 100.2) / 99.6 ≈ -0.00602 (< -threshold)
    assert strategy.generate_signal() == "sell", "Signal should be 'sell' when momentum < -threshold"

    # Step 4: Stable prices - should trigger "hold"
    prices = [100.0] * 10  # Stable prices
    for price in prices:
        strategy.update_price(price)

    # Momentum = (X_n - X_n-1) / X_n where:
    # X_n and X_n-1 are both equal (100.0 average)
    assert strategy.generate_signal() == "hold", "Signal should be 'hold' when momentum is within threshold"
