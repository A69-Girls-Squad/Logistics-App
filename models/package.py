import re
from commands.validation_helpers import try_parse_float


class Package:
    _current_id = 0

    _email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+") #convert a regex pattern into a regex object

    @classmethod
    def _next_id(cls):
        cls._current_id += 1
        return cls._current_id

    def __init__(self, start_location: str, end_location: str, weight: float, customer_email: str):
        self._id = Package._next_id()
        self._start_location = start_location # to create a class of the cities for validation
        self._end_location = end_location# to create a class of the cities for validation
        if weight < 0:
            raise ValueError("Weight can not be negative number")
        self._weight = try_parse_float(weight)
        if not Package._email_regex.fullmatch(customer_email):
            raise ValueError(f"Invalid email address: {customer_email}")
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
Weight: {self._weight:.2f}kg
Customer Email Address: {self._customer_email}
Departure time: {self._departure_time}
Estimated arrival time: {self._estimated_arrival_time}"""


