from datetime import datetime

class ApplicationTime:
    """
    Manages the current application time, allowing for simulation of time in the application.

    This class provides a centralized way to manage and manipulate the current time
    within the application. It supports getting the current time and setting a custom
    time for simulation purposes.

    Attributes:
        _current_app_time (datetime): The current application time.
    """

    _current_app_time = datetime.now()

    @classmethod
    def current(cls):
        """
        Returns the current application time.

        Returns:
            datetime: The current application time.
        """
        return cls._current_app_time

    @classmethod
    def set_current(cls, current_datetime: datetime) -> None:
        """
        Sets the current application time to a specified datetime.

        This method is useful for simulating time changes in the application.

        Args:
            current_datetime (datetime): The datetime to set as the current application time.
        """
        cls._current_app_time = current_datetime