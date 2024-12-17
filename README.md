# Momentum-Based Trading Backtester

This project provides a simple backtesting framework for a momentum-based trading strategy applied to the S&P 500 index and futures data.

## Overview

**Key Features:**
- Fetch 2 weeks of historical 1-minute interval data for S&P 500 index (^GSPC) and futures (ES=F) using `yfinance`.
- Implement a momentum-based strategy:
  - Compute 5-minute rolling momentum on the future.
  - If momentum > 0.0005 → Buy the index.
  - If momentum < -0.0005 → Sell the index.
  - Close position after 10 minutes.
- Incorporate commissions, margin requirements for shorts, and PnL calculations.
- Print real-time trade executions and daily summaries.
- Compute final performance metrics: number of winners/losers, average PnL, geometric mean PnL, Sharpe ratio, and final portfolio value.
- **Portfolio Class**: Manages positions, cash, and trades.
- **Trade Class**: Handles PnL and commission logic.
- Full test coverage for portfolio and trading logic using `pytest`.
## Project Structure

```plaintext
PYTHON-DEV-CASE-1-MAIN/
│
├── .pytest_cache/             # Pytest cache for test runs
├── .venv/                     # Virtual environment
│
├── data/                      # Data directory
│   ├── .gitkeep               # Placeholder for empty directories
│   ├── spx_future.csv         # CSV file for S&P 500 future data
│   └── spx_index.csv          # CSV file for S&P 500 index data
│
├── scripts/                   # Scripts for data processing
│   ├── yfinance_1min_data_example.py           # Example of fetching 1-min data
│   └── yfinance_two_weeks_1min_intervals_data.py # Fetching 2 weeks of 1-min data
│
├── src/                       # Source code directory
│   ├── __pycache__/           # Python bytecode cache
│   ├── __init__.py            # Package initialization
│   └── backtesting/           # Backtesting logic
│       └── definitions.py     # Definitions for backtesting
│
├── tests/                     # Unit tests for the project
│   ├── __pycache__/           # Test cache
│   ├── conftest.py            # Pytest configuration
│   ├── test_definitions.py    # Test definitions
│   ├── test_performance.py    # Test performance metrics
│   ├── test_portfolio.py      # Test portfolio logic
│   ├── test_strategy_signal.py # Test strategy signals
│   └── test_trades.py         # Test trade functionality
│
├── .gitignore                 # Git ignore file
├── poetry.lock                # Poetry lock file
├── pyproject.toml             # Project dependencies and metadata
├── README.md                  # Project documentation
└── requirements.txt           # Project dependencies for pip
```

## Installation

1. **Install Python 3.10 or later**  
   Ensure Python 3.10+ is installed:
   ```sh
   python3.10 --version
 
## ⚙️ Installation

### 1. Clone the repository  
```sh
git clone  git@github.com:Nizalk/Case-Submission-Python-Software-Engineer---November-2024-CROSS-OPTIONS.git
```
---

### 2. Install required dependencies
Unix Systems:
```sh
python3.10 -m venv .venv3.10
source ./.venv3.10/bin/activate
poetry install --sync
```
Windows Systems
```sh
python3.10 -m venv .venv3.10
.\.venv3.10\Scripts\activate
poetry install --sync
```

---

## 🚀 Running the Backtester  

Run the backtester by executing:
```sh
python src\backtesting\run_backtester.py

```
Example of summary generated 
```sh
=== Performance Summary ===
Number of Trades: 50
Winners: 30
Losers: 20
Average PnL: 85.20
Geometric Mean PnL per Trade: 0.0009
Sharpe Ratio: 1.45
Final Portfolio Value: 103500.00
```
## 📊 Statistical Approach

### Key Metrics and Complexity

1. **Geometric Mean PnL**
   - Captures the **compound growth** of trades:
     `````
     G = [(1 + r1) * (1 + r2) * ... * (1 + rn)]^(1/n) - 1
     `````
   - Computational Complexity: **O(n)** (single pass for trade returns).

2. **Sharpe Ratio**
   - Measures **risk-adjusted return**:
     `````
     Sharpe Ratio = Mean(Returns) / StdDev(Returns)
     `````
   - Complexity: **O(n)** for mean and variance in a single pass.

3. **Winners and Losers**
   - Simple categorization in one iteration: **O(n)**.

4. **Memory Efficiency**
   - Trades and metrics are updated incrementally without redundant recalculations.

---
## 🧪 Running the Tests

Run all unit tests in the `tests/` directory using `pytest` or `poetry run pytest`:

## 📈 Example Output

After running the backtester, you will get a summary like:
```sh
==================================================== test session starts ====================================================
collected 4 items

tests/test_portfolio.py ....                                                                                       [100%]

===================================================== 4 passed in 0.10s ====================================================
```

---
## Notes on Complexity
Single Pass Calculations: Metrics like Sharpe Ratio, geometric mean, and win/loss ratios are computed efficiently with single iterations over trade data.
Modularity: Separation of concerns between Portfolio and Trade classes simplifies debugging and extends functionality.
Scalability: The framework can scale to higher-frequency data (e.g., tick data) with minor modifications.

## Contact
For inquiries or suggestions, feel free to reach out:

elkhayirnizar@gmail.com
