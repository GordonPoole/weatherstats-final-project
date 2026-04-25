import logging
from pathlib import Path
import asyncio

from .fetching import DatasetFetcher
from .processing import NumericSummaryProcessor, HumidityRainPatternProcessor
from .storage import JSONStorage
from .visualization import (
    save_humidity_rain_bar_chart,
    save_rainfall_histogram,
    save_correlation_heatmap,
)

logger = logging.getLogger("weather_app")
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(name)s - %(message)s"
)


class WeatherApp:
    def __init__(self, datasets, outdir: Path):
        self.datasets = datasets
        self.outdir = outdir

        self.fetcher = DatasetFetcher(
            datasets.train,
            datasets.test
        )
        self.processor = NumericSummaryProcessor()
        self.humidity_processor = HumidityRainPatternProcessor()
        self.storage = JSONStorage()

    async def run(self, **kwargs):
        preview_rows = kwargs.get("preview_rows", 5)

        logger.info("Starting WeatherApp")

        try:
            self.fetcher.validate()
        except Exception as e:
            logger.error(f"Dataset validation failed: {e}")
            raise

        # ⚡ ASYNC FETCHING
        train_df, test_df = await self.fetcher.load_async()
        logger.info("Processing training data (parallel)")
        summary_df = self.processor.process_parallel(train_df)

        preview_iter = (
            row.to_dict()
            for _, row in summary_df.head(preview_rows).iterrows()
        )

        self.outdir.mkdir(parents=True, exist_ok=True)

        summary_output_path = self.outdir / "summary_preview.json"
        self.storage.save_obj(
            {"preview": list(preview_iter)},
            summary_output_path
        )

        logger.info("Analyzing humidity pattern (rainy vs non-rainy)")
        humidity_pattern = self.humidity_processor.process(train_df)

        humidity_json_path = self.outdir / "humidity_pattern.json"
        self.storage.save_obj(humidity_pattern, humidity_json_path)

        logger.info("Creating charts")
        charts_dir = self.outdir / "charts"

        humidity_chart_path = charts_dir / "humidity_rain_pattern.png"
        save_humidity_rain_bar_chart(
            humidity_pattern["rainy_avg_humidity_3pm"],
            humidity_pattern["non_rainy_avg_humidity_3pm"],
            humidity_chart_path
        )

        rain_hist_path = charts_dir / "rainfall_histogram.png"
        save_rainfall_histogram(train_df, rain_hist_path)

        heatmap_path = charts_dir / "correlation_heatmap.png"
        save_correlation_heatmap(train_df, heatmap_path)

        logger.info("WeatherApp finished successfully")

        return {
            "summary_preview": summary_output_path,
            "humidity_pattern": humidity_json_path,
            "humidity_chart": humidity_chart_path,
            "rainfall_histogram": rain_hist_path,
            "correlation_heatmap": heatmap_path,
        }