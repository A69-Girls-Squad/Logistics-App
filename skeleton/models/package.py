from datetime import datetime
import re
from errors.application_error import ApplicationError
from models.route import Route
from skeleton.commands.validation_helpers import try_parse_float


class Package:
    """
    Represents a package for delivery, including details such as start and end locations, weight,
    customer email, and estimated delivery times.

    Attributes:
        _current_id (int): Class variable that keeps track of the last assigned package ID.
        _email_regex (Pattern): Regular expression pattern for validating customer email addresses.

    Methods:
        next_id() -> int:
            Generates the next unique package ID.

        from_json(data: dict) -> Package:
            Creates a Package instance from a JSON-like dictionary.

        __init__(start_location: str, end_location: str, weight: float, customer_email: str):
            Initializes a package with location, weight, and customer email validations.

        to_json() -> dict:
            Converts the package object into a dictionary for JSON serialization.

        __str__() -> str:
            Returns a readable string representation of the package.

    Properties:
        id (int): Returns the unique package ID.
        start_location (str): Returns the start location of the package.
        end_location (str): Returns the end location of the package.
        weight (float): Returns the weight of the package.
        customer_email (str): Returns the customer's email address.
        departure_time (datetime or None): Returns the departure time of the package.
        estimated_arrival_time (datetime or None): Returns the estimated arrival time.
        is_assigned (bool): Returns whether the package has been assigned to a route.
        route_id (int or None): Returns the route ID associated with the package.

    Raises:
        ValueError: If the start or end location is invalid, weight is negative, or email is invalid.
        ApplicationError: If the start and end locations are the same.
    """
    _current_id = 0
    _email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    @classmethod
    def next_id(cls) -> int:
        """
         Generates and returns the next unique package ID.

         Returns:
             int: The next unique ID.
         """
        cls._current_id += 1
        return cls._current_id

    @classmethod
    def from_json(cls, data):
        """
        Creates a Package instance from a dictionary representation.

        Args:
            data (dict): A dictionary containing package details.

        Returns:
            Package: An instance of the Package class.
        """
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

    def __init__(self, start_location: str, end_location: str, weight: float, customer_email: str):
        """
        Initializes a Package instance with required validations.

        Args:
            start_location (str): The starting location of the package.
            end_location (str): The destination location of the package.
            weight (float): The weight of the package in kilograms.
            customer_email (str): The email address of the recipient.

        Raises:
            ValueError: If the start or end location is invalid, weight is negative, or email format is incorrect.
            ApplicationError: If the start and end locations are the same.
        """
        self._id = Package.next_id()

        if start_location not in Route.CITIES:
            raise ValueError("Location does not exists")
        self._start_location = start_location

        if start_location not in Route.CITIES:
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
    def id(self) -> int:
        """Returns the unique package ID."""
        return self._id

    @property
    def start_location(self) -> str:
        """Returns the start location of the package."""
        return self._start_location

    @property
    def end_location(self) -> str:
        """Returns the end location of the package."""
        return self._end_location

    @property
    def weight(self) -> float:
        """Returns the weight of the package."""
        return self._weight

    @property
    def customer_email(self) -> str:
        """Returns the customer's email address."""
        return self._customer_email

    @property
    def departure_time(self) -> datetime:
        """Returns the departure time of the package."""
        return self._departure_time

    @property
    def estimated_arrival_time(self) -> datetime:
        """Returns the estimated arrival time of the package."""
        return self._estimated_arrival_time

    @property
    def is_assigned(self) -> bool:
        """Returns whether the package is assigned to a route."""
        return self._is_assigned

    @property
    def route_id(self) -> int:
        """Returns the route ID associated with the package."""
        return self._route_id

    def to_json(self) -> dict:
        """
        Converts the package object into a JSON dictionary.

        Returns:
            dict: A dictionary representation of the package.
        """
        return {
            "_id": self._id,
            "_start_location": self._start_location,
            "_end_location": self._end_location,
            "_weight": self._weight,
            "_customer_email": self._customer_email,
            "_departure_time": self._departure_time.isoformat() if self._departure_time else None,
            "_estimated_arrival_time": self._estimated_arrival_time.isoformat() if self._estimated_arrival_time else None,
            "_is_assigned": self._is_assigned,
            "_route_id": self._route_id
            }

    def __str__(self) -> str:
        """
        Returns a readable string representation of the package, including
        its status based on the current time.

        Returns:
            str: A formatted string describing the package.
        """
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
