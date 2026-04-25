class WeatherAppError(Exception):
    """Base class for app specific errors."""


class DatasetNotFoundError(WeatherAppError):
    """Raised when an input dataset path does not exist."""


class InvalidDatasetError(WeatherAppError):
    """Raised when a dataset is missing expected columns or is malformed."""