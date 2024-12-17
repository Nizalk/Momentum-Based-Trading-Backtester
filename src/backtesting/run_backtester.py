import sys
import os
# Ensure the 'src' directory is included in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

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

