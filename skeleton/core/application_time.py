from datetime import datetime

class ApplicationTime:
    _current_app_time = datetime.now()

    @classmethod
    def current(cls):
        return cls._current_app_time

    @classmethod
    def set_current(cls, current_datetime: datetime) -> None:
        cls._current_app_time = current_datetime