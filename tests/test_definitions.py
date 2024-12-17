# tests/test_definitions.py

from src.definitions import SPX_INDEX_DATA, SPX_FUTURE_DATA

def test_definitions():
    assert SPX_INDEX_DATA.suffix == '.csv', "SPX_INDEX_DATA should point to a CSV file"
    assert SPX_FUTURE_DATA.suffix == '.csv', "SPX_FUTURE_DATA should point to a CSV file"
