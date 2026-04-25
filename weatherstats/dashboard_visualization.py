from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


plt.style.use("ggplot")


def prepare_city_data(df: pd.DataFrame, city: str) -> pd.DataFrame:
    required = ["Location", "MinTemp", "MaxTemp", "Rainfall", "Humidity3pm"]

    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    city_df = df[df["Location"] == city].copy()

    if city_df.empty:
        raise ValueError(f"No data found for city: {city}")

    numeric_cols = [
        "MinTemp",
        "MaxTemp",
        "Rainfall",
        "Humidity3pm",
        "Pressure3pm",
        "Temp9am",
        "Temp3pm",
        "WindGustSpeed"
    ]

    for col in numeric_cols:
        if col in city_df.columns:
            city_df[col] = pd.to_numeric(city_df[col], errors="coerce")

    city_df = city_df.reset_index(drop=True)
    city_df["Observation"] = city_df.index + 1

    return city_df


def make_temperature_chart(df: pd.DataFrame, city: str, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    city_df = prepare_city_data(df, city)
    city_df = city_df.dropna(subset=["MinTemp", "MaxTemp"])

    city_df["MinSmooth"] = city_df["MinTemp"].rolling(25).mean()
    city_df["MaxSmooth"] = city_df["MaxTemp"].rolling(25).mean()

    plt.figure(figsize=(12, 6))

    plt.plot(
        city_df["Observation"],
        city_df["MinSmooth"],
        label="Min Temp",
        linewidth=2.5
    )

    plt.plot(
        city_df["Observation"],
        city_df["MaxSmooth"],
        label="Max Temp",
        linewidth=2.5
    )

    plt.title(f"Temperature Patterns - {city}", fontsize=16, weight="bold")
    plt.xlabel("Observation Number")
    plt.ylabel("Temperature (°C)")
    plt.grid(alpha=.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=170)
    plt.close()

    return outpath


def make_rainfall_chart(df: pd.DataFrame, city: str, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    city_df = prepare_city_data(df, city)
    city_df = city_df.dropna(subset=["Rainfall"])

    plt.figure(figsize=(12, 6))

    plt.hist(
        city_df["Rainfall"],
        bins=35,
        edgecolor="black",
        alpha=.85
    )

    avg_rain = city_df["Rainfall"].mean()

    plt.axvline(
        avg_rain,
        linestyle="--",
        linewidth=2,
        label=f"Mean: {avg_rain:.2f} mm"
    )

    plt.title(f"Rainfall Distribution - {city}", fontsize=16, weight="bold")
    plt.xlabel("Rainfall (mm)")
    plt.ylabel("Frequency")
    plt.grid(alpha=.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=170)
    plt.close()

    return outpath


def make_extreme_chart(df: pd.DataFrame, city: str, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    city_df = prepare_city_data(df, city)
    city_df = city_df.dropna(subset=["MinTemp", "MaxTemp", "Rainfall", "Humidity3pm"])

    labels = [
        "Max Temp",
        "Min Temp",
        "Rainfall",
        "Humidity"
    ]

    values = [
        city_df["MaxTemp"].max(),
        city_df["MinTemp"].min(),
        city_df["Rainfall"].max(),
        city_df["Humidity3pm"].max()
    ]

    units = ["°C", "°C", " mm", "%"]

    plt.figure(figsize=(11, 6))

    bars = plt.bar(
        labels,
        values
    )

    for i, bar in enumerate(bars):
        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}{units[i]}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    plt.title(f"Weather Extremes - {city}", fontsize=16, weight="bold")
    plt.ylabel("Measured Value")
    plt.grid(axis="y", alpha=.25)
    plt.tight_layout()
    plt.savefig(outpath, dpi=170)
    plt.close()

    return outpath