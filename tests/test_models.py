import pytest
from pathlib import Path
from weatherstats.models import DatasetPaths, NumericFields
from weatherstats.exceptions import DatasetNotFoundError

def test_validate_success(tmp_path):
    train_file = tmp_path / "train.csv"
    test_file = tmp_path / "test.csv"

    train_file.write_text("data")
    test_file.write_text("data")

    paths = DatasetPaths(train=train_file, test=test_file)

    paths.validate()


def test_validate_missing_train(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("data")

    paths = DatasetPaths(train=tmp_path / "missing.csv", test=test_file)

    with pytest.raises(DatasetNotFoundError):
        paths.validate()


def test_validate_missing_test(tmp_path):
    train_file = tmp_path / "train.csv"
    train_file.write_text("data")

    paths = DatasetPaths(train=train_file, test=tmp_path / "missing.csv")

    with pytest.raises(DatasetNotFoundError):
        paths.validate()


def test_numericfields_default_contains_expected_fields():
    fields = NumericFields.default()

    assert isinstance(fields, NumericFields)
    assert "MinTemp" in fields.fields
    assert "MaxTemp" in fields.fields
    assert "Temp3pm" in fields.fields


def test_numericfields_is_immutable():
    fields = NumericFields.default()

    with pytest.raises(AttributeError):
        fields.fields = frozenset({"NewField"})