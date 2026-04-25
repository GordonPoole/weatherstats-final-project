from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet

from .exceptions import DatasetNotFoundError


@dataclass(frozen=True, slots=True)
class DatasetPaths:
    train: Path
    test: Path

    def validate(self) -> None:
        if not self.train.exists():
            raise DatasetNotFoundError(f"Training CSV not found: {self.train}")
        if not self.test.exists():
            raise DatasetNotFoundError(f"Test CSV not found: {self.test}")


@dataclass(frozen=True, slots=True)
class NumericFields:
    fields: FrozenSet[str]

    @staticmethod
    def default() -> "NumericFields":
        return NumericFields(fields=frozenset({
            "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
            "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm",
            "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
            "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm",
        }))