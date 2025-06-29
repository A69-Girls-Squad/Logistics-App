import re
from datetime import datetime
from errors.application_error import ApplicationError
from core.application_time import ApplicationTime
from commands.validation_helpers import try_parse_float
from models.route import Route
from interface_menu import TABLE_SEP, ROW_SEP


class Package:
    """
    Represents a package with details such as start and end locations, weight, customer email,
    and tracking information like departure time, estimated arrival time, and assignment status.

    Attributes:
        _current_id (int): A class-level counter for generating unique package IDs.
        _email_regex (Pattern): A compiled regex pattern for validating email addresses.
    """
    _current_id = 0
    _email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    TABLE_SEP = "-" * 16 + "|" + "-" * 43
    ROW_SEP = "\n" + "=" * 60

    @classmethod
    def next_id(cls) -> int:
        """
         Generates and returns the next unique package ID.

         Returns:
             int: The next unique ID.
         """
        cls._current_id += 1
        return cls._current_id


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
            raise ValueError("Start location does not exist")
        self._start_location = start_location

        if end_location not in Route.CITIES:
            raise ValueError("End location does not exist")
        if start_location == end_location:
            raise ApplicationError("Start location can not be the same as End location")
        self._end_location = end_location

        if weight < 0:
            raise ValueError("Weight can not be a negative number")
        self._weight = try_parse_float(weight)

        if not Package._email_regex.fullmatch(customer_email):
            raise ValueError(f"Invalid email address: {customer_email}")
        self._customer_email = customer_email

        self._departure_time = None
        self._estimated_arrival_time = None
        self._is_assigned = False
        self._route_id = None


    @classmethod
    def from_json(cls, data: dict):
        """
         Creates a Package instance from a JSON-compatible dictionary.

         Args:
             data (dict): A dictionary containing package details.

         Returns:
             Package: An instance of the Package class.
         """
        package = cls(
            start_location=data["start_location"],
            end_location=data["end_location"],
            weight=data["weight"],
            customer_email=data["customer_email"]
        )
        package._departure_time = (
            datetime.fromisoformat(data["departure_time"]) if data["departure_time"] else None
        )
        package._estimated_arrival_time = (
            datetime.fromisoformat(data["estimated_arrival_time"]) if data["estimated_arrival_time"] else None
        )
        package._is_assigned = data["is_assigned"]
        package._route_id = data["route_id"]

        return package

    def to_json(self) -> dict:
        """
        Converts the package object into a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the package.
        """
        return {
            "id": self._id,
            "start_location": self._start_location,
            "end_location": self._end_location,
            "weight": self._weight,
            "customer_email": self._customer_email,
            "departure_time": self._departure_time.isoformat() if self._departure_time else None,
            "estimated_arrival_time": self._estimated_arrival_time.isoformat() if self._estimated_arrival_time else None,
            "is_assigned": self._is_assigned,
            "route_id": self._route_id
            }

    @property
    def id(self) -> int:
        """
        Gets the unique identifier of the package.

        Returns:
            int: The package ID.
        """
        return self._id

    @property
    def start_location(self) -> str:
        """
        Gets the start location of the package.

        Returns:
            str: The start location.
        """
        return self._start_location

    @property
    def end_location(self) -> str:
        """
         Returns the end location of the package.

         Returns:
             str: The end location.
         """
        return self._end_location

    @property
    def weight(self) -> float:
        """
        Gets the weight of the package.

        Returns:
            float: The weight of the package in kilograms.
        """
        return self._weight

    @property
    def customer_email(self) -> str:
        """
        Gets the customer's email address.

        Returns:
            str: The customer's email address.
        """
        return self._customer_email

    @property
    def departure_time(self) -> datetime:
        """
        Gets the departure time of the package.

        Returns:
            datetime: The departure time.
        """
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: datetime) -> None:
        """
        Sets the departure time of the package.

        Args:
            value (datetime): The departure time to set.
        """
        self._departure_time = value

    @property
    def estimated_arrival_time(self) -> datetime:
        """
        Gets the estimated arrival time of the package.

        Returns:
            datetime: The estimated arrival time.
        """
        return self._estimated_arrival_time

    @estimated_arrival_time.setter
    def estimated_arrival_time(self, value: datetime) -> None:
        """
        Sets the estimated arrival time of the package.

        Args:
            value (datetime): The estimated arrival time to set.
        """
        self._estimated_arrival_time = value

    @property
    def is_assigned(self) -> bool:
        """
        Gets whether the package is assigned to a route.

        Returns:
            bool: True if the package is assigned, False otherwise.
        """
        return self._is_assigned

    @is_assigned.setter
    def is_assigned(self, value: bool) -> None:
        """
        Sets whether the package is assigned to a route.

        Args:
            value (bool): True if the package is assigned, False otherwise.
        """
        self._is_assigned = value

    @property
    def route_id(self) -> int:
        """
        Gets the route ID associated with the package.

        Returns:
            int: The route ID.
        """
        return self._route_id

    @route_id.setter
    def route_id(self, value) -> None:
        """
        Sets the route ID associated with the package.

        Args:
            value (int): The route ID to set.
        """
        self._route_id = value

    def __str__(self) -> str:
        """
         Returns a readable string representation of the package.

         Returns:
             str: A formatted string describing the package.
         """
        if self.departure_time:
            if ApplicationTime.current() < self.departure_time:
                status = "Awaiting Dispatch"
            elif ApplicationTime.current() < self.estimated_arrival_time:
                status = "In Transit"
            else:
                status = "Delivered"
            status += (f"\nDeparture time: | {self._departure_time.isoformat(sep=" ", timespec="minutes")}"
                       f"\nArrival time:   | "
                       f"{self._estimated_arrival_time.isoformat(sep=" ", timespec="minutes")}"
                       f"\nRoute ID:       | {self.route_id}")
        else:
            status = "Not assigned"

        return (f"{ROW_SEP}\nPACKAGE DETAILS:\n{TABLE_SEP}"
                f"\nID:             | {self._id}\n{TABLE_SEP}"
                f"\nStart Location: | {self._start_location}\n{TABLE_SEP}"
                f"\nEnd Location:   | {self._end_location}\n{TABLE_SEP}"
                f"\nWeight:         | {self._weight:.2f} kg\n{TABLE_SEP}"
                f"\nCustomer Email: | {self._customer_email}\n{TABLE_SEP}"
                f"\nPackage Status: | {status}\n{TABLE_SEP}")
