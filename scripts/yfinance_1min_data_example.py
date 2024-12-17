import pandas as pd
import seaborn as sns
import yfinance as yf
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.definitions import SPX_INDEX_DATA, SPX_FUTURE_DATA

sns.set_theme()


def download_minute_data(symbol: str) -> pd.DataFrame:
    ticker: yf.Ticker = yf.Ticker(symbol)
    data: pd.DataFrame = ticker.history(
        start="2024-11-25",
        end="2024-11-30",
        interval="1m",
    )
    print(data.head())
    print(data.tail())
    num_rows: int = len(data)
    num_days: int = pd.Series(data.index.date).nunique()
    print(f"Total rows: {num_rows:,}")
    print(f"Days: {num_days}")
    return data


if __name__ == "__main__":
    spx_index_data: pd.DataFrame = download_minute_data(symbol="^GSPC")
    spx_index_data.to_csv(SPX_INDEX_DATA)

    spx_future_data: pd.DataFrame = download_minute_data(symbol="ES=F")
    spx_future_data.to_csv(SPX_FUTURE_DATA)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.plot(spx_future_data.index, spx_future_data["Close"], label="Close E-Mini")
    plt.plot(spx_index_data.index, spx_index_data["Close"], label="Close SPX")
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Close Price (USD)", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.show()

