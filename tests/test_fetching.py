import pytest
import pandas as pd
from pathlib import Path
from weatherstats.fetching import DatasetFetcher


def test_validate_success(tmp_path):
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"

    train.write_text("a,b\n1,2")
    test.write_text("a,b\n3,4")

    fetcher = DatasetFetcher(train, test)
    fetcher.validate()


def test_validate_missing_train(tmp_path):
    test = tmp_path / "test.csv"
    test.write_text("a,b\n3,4")

    fetcher = DatasetFetcher(tmp_path / "missing.csv", test)

    with pytest.raises(FileNotFoundError):
        fetcher.validate()


def test_validate_missing_test(tmp_path):
    train = tmp_path / "train.csv"
    train.write_text("a,b\n1,2")

    fetcher = DatasetFetcher(train, tmp_path / "missing.csv")

    with pytest.raises(FileNotFoundError):
        fetcher.validate()

def test_load_returns_dataframes(tmp_path):
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"

    train.write_text("a,b\n1,2\n3,4")
    test.write_text("a,b\n5,6")

    fetcher = DatasetFetcher(train, test)
    train_df, test_df = fetcher.load()

    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    assert len(train_df) == 2
    assert len(test_df) == 1


def test_load_coerces_non_numeric_to_nan(tmp_path):
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"

    train.write_text("a,b\n1,x\n3,4")
    test.write_text("a,b\n5,6")

    fetcher = DatasetFetcher(train, test)
    train_df, _ = fetcher.load()
    assert pd.isna(train_df.loc[0, "b"])