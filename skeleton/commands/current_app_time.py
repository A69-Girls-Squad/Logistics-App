from datetime import datetime, timedelta

class AppTime:
    _current_app_time = datetime.now()

    @staticmethod
    def current():
        return AppTime._current_app_time

    @staticmethod
    def set_current(days: int):
        AppTime._current_app_time += timedelta(days=days)