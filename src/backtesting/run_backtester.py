import sys
import os
# Adjust the path if necessary so that Python can find your src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backtesting.backtester import Backtester
from src.backtesting.strategies.momentumstrategy import MomentumStrategy


if __name__ == "__main__":
    # Instantiate your strategy
    strategy = MomentumStrategy(threshold=0.0005)

    # Instantiate the backtester with the chosen strategy
    backtester = Backtester(strategy=strategy, initial_cash=100000.0)

    # Load your data from CSV files - ensure they exist in the data/ directory
    index_data_path = "data/spx_index.csv"
    future_data_path = "data/spx_future.csv"

    backtester.load_data(index_file=index_data_path, future_file=future_data_path)

    # Run the backtest
    backtester.run()
    backtester.print_performance()  # Compute final stats and print them

