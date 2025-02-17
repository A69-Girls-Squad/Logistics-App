from datetime import datetime
import re
from errors.application_error import ApplicationError
from models.route import Route
from skeleton.commands.validation_helpers import try_parse_float


class Package:
    _current_id = 0

    _email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @classmethod
    def next_id(cls):
        cls._current_id += 1
        return cls._current_id

    @classmethod
    def from_json(cls, data):
        package = cls(
            start_location=data["_start_location"],
            end_location=data["_end_location"],
            weight=data["_weight"],
            customer_email=data["_customer_email"]
        )
        package._departure_time = (
            datetime.fromisoformat(data["_departure_time"]) if data["_departure_time"] else None
        )
        package._estimated_arrival_time = (
            datetime.fromisoformat(data["_estimated_arrival_time"]) if data["_estimated_arrival_time"] else None
        )
        package._is_assigned = data["_is_assigned"]

        return package
    '''
    Represents a package that is assigned to a delivery route.

    Attributes:
      _id (int): The unique identifier of the package.
      _start_location (str): The starting location of the package.
      _end_location (str): The destination of the package.
      _weight (float): The weight of the package in kilograms.
    '''

    def __init__(self, start_location: str, end_location: str, weight: float, customer_email: str):
        self._id = Package.next_id()

        if not start_location in Route.CITIES:
            raise ValueError("Location does not exists")
        self._start_location = start_location

        if not start_location in Route.CITIES:
            raise ValueError("Location does not exists")
        if start_location == end_location:
            raise ApplicationError("Start location can not be the same as End location")
        self._end_location = end_location

        if weight < 0:
            raise ValueError("Weight can not be negative number")
        self._weight = try_parse_float(weight)
        if not Package._email_regex.fullmatch(customer_email):
            raise ValueError(f"Invalid email address: {customer_email}")
        self._customer_email = customer_email
        self._departure_time = None
        self._estimated_arrival_time = None
        self._is_assigned = False
        self._route_id = None


    @property
    def id(self):
        return self._id

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
    def is_assigned(self):
        return self._is_assigned

    @property
    def route_id(self):
        return self._route_id

    def to_json(self):
        return {
            "_id": self._id,
            "_start_location": self._start_location,
            "_end_location": self._end_location,
            "_weight": self._weight,
            "_customer_email": self._customer_email,
            "_departure_time": self._departure_time.isoformat() if self._departure_time else None,
            "_estimated_arrival_time": self._estimated_arrival_time.isoformat() if self._estimated_arrival_time else None,
            "_is_assigned": self._is_assigned }
            # Route ID

    def __str__(self):
        if datetime.now() < self.departure_time:
            status = "Awaiting Dispatch"
        elif self.departure_time <= datetime.now() < self.estimated_arrival_time:
            status = "In Transit"
        else:
            status = "Delivered"

        return (f"ID: {self._id}"
                f"\nStart Location: {self._start_location})"
                f"\nEnd Location: {self._end_location}"
                f"\nWeight: {self._weight:.2f}kg"
                f"\nCustomer Email Address: {self._customer_email}"
                f"\nDeparture time: {self._departure_time}"
                f"\nEstimated arrival time: {self._estimated_arrival_time}"
                f"\nPackage status: {status}")

