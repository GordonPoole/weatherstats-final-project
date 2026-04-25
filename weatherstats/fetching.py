from pathlib import Path
import pandas as pd
import asyncio


class DatasetFetcher:
    def __init__(self, train_path: Path, test_path: Path):
        self.train_path = train_path
        self.test_path = test_path

    def validate(self):
        if not self.train_path.exists():
            raise FileNotFoundError("Training file not found")
        if not self.test_path.exists():
            raise FileNotFoundError("Test file not found")

    def load(self):
        """
        Sequential (blocking) version.
        Kept for comparison and fallback.
        """
        train_df = pd.read_csv(self.train_path)
        test_df = pd.read_csv(self.test_path)

        for col in train_df.columns:
            train_df[col] = pd.to_numeric(train_df[col], errors="coerce")

        return train_df, test_df

    async def load_async(self):
        """
        Asynchronous (non-blocking) version using asyncio.
        Runs file loading in separate threads to avoid blocking the event loop.
        """
        loop = asyncio.get_running_loop()

        # Run both file reads concurrently
        train_future = loop.run_in_executor(None, pd.read_csv, self.train_path)
        test_future = loop.run_in_executor(None, pd.read_csv, self.test_path)

        train_df, test_df = await asyncio.gather(train_future, test_future)

        for col in train_df.columns:
            train_df[col] = pd.to_numeric(train_df[col], errors="coerce")

        return train_df, test_df
    