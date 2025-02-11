from datetime import datetime

class EventLog():
    _format = '%m/%d/%Y, %H:%M:%S'

    def __init__(self, description: str):
        if not description or description.isspace():
            raise ValueError('Description cant be empty')
            
        self._description = description
        self._timestamp = datetime.now()

    @property
    def description(self):
        return self._description

    @property
    def timestamp(self):
        return self._timestamp

    def info(self):
        return f'[{self.timestamp.strftime(EventLog._format)}] {self.description}'