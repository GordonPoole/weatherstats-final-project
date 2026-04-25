import pandas as pd
import pytest
from weatherstats.processing import NumericSummaryProcessor


def test_iter_numeric_columns_only_numeric():
    df = pd.DataFrame({
        "temp": [10, 20, 30],
        "humidity": [50, 60, 70],
        "city": ["A", "B", "C"]
    })

    processor = NumericSummaryProcessor()
    columns = list(processor.iter_numeric_columns(df))
    col_names = [col for col, _ in columns]
    assert "temp" in col_names
    assert "humidity" in col_names
    assert "city" not in col_names


def test_iter_numeric_columns_drops_nan():
    df = pd.DataFrame({
        "temp": [10, None, 30]
    })

    processor = NumericSummaryProcessor()
    columns = list(processor.iter_numeric_columns(df))

    col, series = columns[0]

    assert series.tolist() == [10, 30]

def test_process_returns_correct_summary():
    df = pd.DataFrame({
        "temp": [10, 20, 30],
        "humidity": [40, 50, 60],
        "city": ["A", "B", "C"]
    })

    processor = NumericSummaryProcessor()
    result = processor.process(df)
    assert len(result) == 2
    temp_row = result[result["column"] == "temp"].iloc[0]
    assert temp_row["mean"] == 20
    assert temp_row["min"] == 10
    assert temp_row["max"] == 30
    assert temp_row["count"] == 3


def test_process_empty_dataframe():
    df = pd.DataFrame()

    processor = NumericSummaryProcessor()
    result = processor.process(df)
    assert result.empty