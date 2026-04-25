from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def save_humidity_rain_bar_chart(rainy_avg: float, dry_avg: float, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.bar(
        ["Rainy (Rainfall>0)", "Non-rainy (Rainfall=0)"],
        [rainy_avg, dry_avg]
    )
    plt.title("Average 3pm Humidity: Rainy vs Non-Rainy Days")
    plt.ylabel("Average Humidity")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

    return outpath


def save_rainfall_histogram(df: pd.DataFrame, outpath: Path, bins: int = 50) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    if "Rainfall" not in df.columns:
        raise KeyError("Expected 'Rainfall' column for rainfall histogram.")

    plt.figure()
    plt.hist(df["Rainfall"].dropna(), bins=bins)
    plt.title("Rainfall Distribution")
    plt.xlabel("Rainfall")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

    return outpath


def save_correlation_heatmap(df: pd.DataFrame, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)

    numeric_df = df.select_dtypes(include="number")

    numeric_df = numeric_df.drop(columns=["row ID", "Location"], errors="ignore")

    if numeric_df.shape[1] == 0:
        raise ValueError("No numeric columns found for correlation heatmap.")

    corr = numeric_df.corr(numeric_only=True)
    corr = corr.fillna(0)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=False)
    plt.title("Correlation Heatmap (Numeric Variables)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()

    return outpath