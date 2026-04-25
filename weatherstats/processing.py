import pandas as pd
from functools import reduce
from multiprocessing import Pool, cpu_count


def process_numeric_column(args):
    """
    Helper function for multiprocessing.
    Processes a single numeric column.
    """
    col, series = args

    return {
        "column": col,
        "mean": float(series.mean()),
        "min": float(series.min()),
        "max": float(series.max()),
        "count": int(series.count())
    }


class NumericSummaryProcessor:
    def iter_numeric_columns(self, df: pd.DataFrame):
        numeric_df = df.select_dtypes(include="number")
        for col in numeric_df.columns:
            yield col, numeric_df[col].dropna()

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sequential version (baseline)
        """
        rows = []

        for col, series in self.iter_numeric_columns(df):
            rows.append({
                "column": col,
                "mean": float(series.mean()),
                "min": float(series.min()),
                "max": float(series.max()),
                "count": int(series.count())
            })

        return pd.DataFrame(rows)

    def process_parallel(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parallel version using multiprocessing.
        Each column is processed on a separate CPU core.
        """
        tasks = list(self.iter_numeric_columns(df))

        with Pool(cpu_count()) as pool:
            results = pool.map(process_numeric_column, tasks)

        return pd.DataFrame(results)


class HumidityRainPatternProcessor:
    """
    Compares average Humidity3pm on rainy vs non-rainy days.

    Rainy day definition: Rainfall > 0

    Uses functional programming:
      - map + lambda
      - filter + lambda
      - reduce + lambda
    """

    def process(self, df: pd.DataFrame) -> dict:
        if "Rainfall" not in df.columns:
            raise KeyError("Expected 'Rainfall' column in dataset.")
        if "Humidity3pm" not in df.columns:
            raise KeyError("Expected 'Humidity3pm' column in dataset.")

        working = df[["Rainfall", "Humidity3pm"]].copy()

        # map + lambda
        working["Rainy"] = working["Rainfall"].map(
            lambda x: 1 if pd.notna(x) and x > 0 else 0
        )

        filtered_df = working[["Humidity3pm", "Rainy"]].dropna()
        rows = list(filtered_df.values)

        # filter + lambda
        rainy_rows = list(filter(lambda row: row[1] == 1, rows))
        dry_rows = list(filter(lambda row: row[1] == 0, rows))

        # map + lambda
        rainy_humidity = list(map(lambda row: float(row[0]), rainy_rows))
        dry_humidity = list(map(lambda row: float(row[0]), dry_rows))

        # reduce + lambda
        rainy_total = reduce(lambda a, b: a + b, rainy_humidity, 0.0)
        dry_total = reduce(lambda a, b: a + b, dry_humidity, 0.0)

        rainy_avg = (rainy_total / len(rainy_humidity)) if rainy_humidity else float("nan")
        dry_avg = (dry_total / len(dry_humidity)) if dry_humidity else float("nan")

        return {
            "definition": "Rainy day = Rainfall > 0",
            "rainy_count": len(rainy_humidity),
            "non_rainy_count": len(dry_humidity),
            "rainy_avg_humidity_3pm": rainy_avg,
            "non_rainy_avg_humidity_3pm": dry_avg
        }
    