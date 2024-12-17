import pandas as pd
import yfinance as yf
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.definitions import SPX_INDEX_DATA, SPX_FUTURE_DATA

def download_minute_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Download approximately two weeks of 1-minute interval data by splitting
    the request into two chunks due to Yahoo Finance limitations.

    :param symbol: The ticker symbol to fetch data for.
    :param start: Start date as a string (YYYY-MM-DD).
    :param end: End date as a string (YYYY-MM-DD).
    :return: A pandas DataFrame with the concatenated data.
    """
    # Convert to datetime
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    # To fetch two weeks, split into two ~1-week periods due to Yahoo limit:
    mid_dt = start_dt + timedelta(days=7)

    # First chunk (7 days)
    first_chunk = yf.Ticker(symbol).history(start=start_dt, end=mid_dt, interval="1m")
    # Second chunk (next 7 days)
    second_chunk = yf.Ticker(symbol).history(start=mid_dt, end=end_dt, interval="1m")

    # Concatenate the two chunks
    data = pd.concat([first_chunk, second_chunk])

    # Check if empty
    if data.empty:
        print(f"No data returned for {symbol} from {start} to {end}.")
        return data

    # Remove timezone if present
    # Some recent versions of yfinance might return a DatetimeIndex without a tz
    if hasattr(data.index, 'tz') and data.index.tz is not None:
        data = data.tz_localize(None)

    # Print some diagnostics
    print(f"Sample data for {symbol}:")
    print(data.head())
    print(data.tail())

    num_rows = len(data)
    num_days = pd.Series(data.index.date).nunique()
    print(f"Total rows for {symbol}: {num_rows:,}")
    print(f"Days covered for {symbol}: {num_days}")

    return data


if __name__ == "__main__":
    # Choose a recent two-week window in the past.
    # For example: The last 14 days from today's date
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=14)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # Download S&P 500 Index data (^GSPC)
    spx_index_data = download_minute_data(symbol="^GSPC", start=start_str, end=end_str)
    if not spx_index_data.empty:
        spx_index_data.to_csv(SPX_INDEX_DATA)

    # Download S&P 500 Future data (ES=F)
    spx_future_data = download_minute_data(symbol="ES=F", start=start_str, end=end_str)
    if not spx_future_data.empty:
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
