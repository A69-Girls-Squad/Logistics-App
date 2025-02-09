class Package:
    _current_id = 0

    @classmethod
    def _next_id(cls):
        cls._current_id += 1
        return cls._current_id

    def __init__(self, start_location: str, end_location: str, weight: float, customer_email: str):
        self._id = Package._next_id()
        self._start_location = start_location
        self._end_location = end_location
        self._weight = weight
        self._customer_email = customer_email
        self._departure_time = None
        self._estimated_arrival_time = None
        self._is_assigned = False
        self._route = None #?


    @property
    def start_location(self):
        return self._start_location

    @property
    def end_location(self):
        return self._end_location

    @property
    def weight(self):
        return self._weight

    @property
    def customer_email(self):
        return self._customer_email

    @property
    def departure_time(self):
        return self._departure_time

    @property
    def estimated_arrival_time(self):
        return self._estimated_arrival_time

    @property
    def route(self):
        return self._route


    def __str__(self):
        return f"""ID: {self._id}
Start Location: {self._start_location}
End Location {self._end_location}
Weight: {self._weight}kg
Customer Email Address: {self._customer_email}
Departure time: {self._departure_time}
Estimated arrival time: {self._estimated_arrival_time}"""


