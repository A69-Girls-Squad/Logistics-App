from datetime import datetime, timedelta
from core.application_time import ApplicationTime
from errors.application_error import ApplicationError
from models.constants.distances import Distance
from models.truck import Truck


class Route:
    """
    Represents a delivery route with multiple stops, including details such as locations,
    departure time, assigned truck, packages, and estimated arrival times.

    Attributes:
        CITIES (list): A list of valid cities for the route, derived from `Distance.DISTANCES`.
        AVERAGE_SPEED (int): The average speed of the truck in kilometers per hour.
        LOCATIONS_SEPARATOR (str): The separator used to split locations in the input string.
        REQUIRED_DATE_FORMAT (str): The required format for the departure time string.
        STATUS_CREATED (str): Status indicating the route has been created but not yet departed.
        STATUS_IN_PROGRESS (str): Status indicating the route is currently in progress.
        STATUS_FINISHED (str): Status indicating the route has been completed.
        _current_id (int): A class-level counter for generating unique route IDs.
    """

    CITIES = list(Distance.DISTANCES)
    AVERAGE_SPEED = 87
    LOCATIONS_SEPARATOR = ","
    REQUIRED_DATE_FORMAT = "%Y-%m-%d %H:%M"

    STATUS_CREATED = "Created"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_FINISHED = "Finished"

    _current_id = 0

    @classmethod
    def next_id(cls) -> int:
        """
         Generates and returns the next unique package ID.

         Returns:
             int: The next unique ID.
         """
        cls._current_id += 1
        return cls._current_id

    def __init__(self, locations: str, departure_time: str):
        """
        Initializes a Route instance with the provided locations and departure time.

        Args:
            locations (str): A string of locations separated by `LOCATIONS_SEPARATOR`.
            departure_time (str): The departure time in the format `REQUIRED_DATE_FORMAT`.

        Raises:
            ApplicationError: If the locations or departure time are invalid.
        """
        self.locations = locations
        self.departure_time = departure_time

        self._id = Route.next_id()
        self._assigned_truck_id = None
        self.assigned_truck_capacity = None
        self._assigned_packages_ids = []
        self.load = 0
        self._stops = {}
        if isinstance(self._locations, list):
            self.calculating_estimated_arrival_times()

    @classmethod
    def from_json(cls, data: dict):
        """
        Creates a Route instance from a JSON-compatible dictionary.

        Args:
            data (dict): A dictionary containing route details, including:
                - locations (str): A string of locations separated by commas.
                - departure_time (str): The departure time in the REQUIRED_DATE_FORMAT.
                - _id (str): The route's unique identifier.
                - _assigned_truck_id (int or None): The ID of the assigned truck.
                - _assigned_package_ids (list): A list of assigned package IDs.
                - _load (float): The total load weight.
                - _stops (dict): A dictionary mapping locations to estimated arrival times.

        Returns:
            Route: An instance of the Route class.
        """
        route = cls(
            locations=data["locations"],
            departure_time="2030-02-23T09:00:00" #Bug, to fix in the future
        )
        route._id = data.get("id", route._id)
        route.locations = data["locations"]
        route._departure_time = (
            datetime.fromisoformat(data["departure_time"]) if data["departure_time"] else None
        )
        route._assigned_truck_id = data.get("assigned_truck_id", None)
        route._assigned_packages_ids = data.get("assigned_package_ids", [])
        route._load = data.get("load", 0)

        return route

    def to_json(self) -> dict:
        """
        Converts the Route object into a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the route, including:
                - locations (str): The locations string.
                - departure_time (str): The departure time in REQUIRED_DATE_FORMAT.
                - id (str): The route's unique identifier.
                - assigned_truck_id (int or None): The ID of the assigned truck.
                - assigned_package_ids (list): The list of assigned package IDs.
                - load (float): The total load weight.
                - stops (dict): A dictionary mapping locations to estimated arrival times (as ISO strings).
        """
        return {
            "locations": self.LOCATIONS_SEPARATOR.join(self.locations),
            "departure_time": self._departure_time.isoformat() if self._departure_time else None,
            "id": self._id,
            "assigned_truck_id": self._assigned_truck_id,
            "assigned_package_ids": self._assigned_packages_ids,
            "load": self._load,
            "stops": {loc: time.isoformat() for loc, time in self._stops.items()}
        }

    @property
    def locations(self) -> tuple:
        """
        Gets the locations of the route as a tuple.

        Returns:
            tuple: A tuple of location names.
        """
        return tuple(self._locations)

    @locations.setter
    def locations(self, value: str) -> None:
        """
        Sets the locations of the route.

        Args:
            value (str): A string of locations separated by `LOCATIONS_SEPARATOR`.

        Raises:
            ApplicationError: If the locations are invalid, contain duplicates, or are too few.
        """
        if not isinstance(value, str):
            raise ApplicationError("Invalid locations")

        if self.LOCATIONS_SEPARATOR not in value:
            raise ApplicationError(f"Locations should be separated by \"{self.LOCATIONS_SEPARATOR}\"")
        value = value.split(self.LOCATIONS_SEPARATOR)

        for location in value:
            if location not in self.CITIES:
                raise ApplicationError(f"Invalid location: {location}.")

        for i in range(len(value)-1):
            if value[i] == value[i+1]:
                raise ApplicationError("Consecutive duplicate locations not allowed!")

        if len(value) < 2:
            raise ApplicationError("Too few locations!")

        self._locations = value

    @property
    def departure_time(self) -> datetime:
        """
        Gets the departure time of the route.

        Returns:
            datetime: The departure time as a `datetime` object.
        """
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: str) -> None:
        """
        Sets the departure time of the route.

        Args:
            value (str): The departure time in the format `REQUIRED_DATE_FORMAT`.

        Raises:
            ApplicationError: If the departure time is in the past or the format is invalid.
        """
        try:
            departure_time = datetime.fromisoformat(value)
            if departure_time < ApplicationTime.current():
                raise ApplicationError("Departure time must be in the future!")
            self._departure_time = departure_time
        except ValueError:
            raise ApplicationError(f"Departure time {value} "
                                   f"does not match the format {self.REQUIRED_DATE_FORMAT}")
    @property
    def id(self) -> int:
        """
        Gets the unique identifier of the route.

        Returns:
            int: The unique identifier of the route.
        """
        return self._id

    @property
    def assigned_truck_id(self) -> int:
        """
        Gets the ID of the truck assigned to the route.

        Returns:
            int or None: The ID of the assigned truck, or `None` if no truck is assigned.
        """
        return self._assigned_truck_id

    @assigned_truck_id.setter
    def assigned_truck_id(self, value: Truck) -> None:
        """
        Sets the ID of the truck assigned to the route.

        Args:
            value (Truck): The truck to assign to the route.
        """
        self._assigned_truck_id = value

    @property
    def assigned_packages_ids(self) -> tuple:
        """
        Gets the IDs of the packages assigned to the route.

        Returns:
            tuple: A tuple of package IDs.
        """
        return tuple(self._assigned_packages_ids)

    @property
    def load(self) -> int:
        """
        Gets the total load weight of the route.

        Returns:
            float: The total load weight in kilograms.
        """
        return self._load

    @load.setter
    def load(self, value: int) -> None:
        """
        Sets the total load weight of the route.

        Args:
            value (int): The total load weight in kilograms.
        """
        self._load = value

    @property
    def stops(self) -> dict:
        """
        Gets the estimated arrival times for each stop along the route.

        Returns:
            dict: A dictionary mapping location names to estimated arrival times.
        """
        self.calculating_estimated_arrival_times()
        return self._stops

    @property
    def distance(self) -> int:
        """
         Calculates the total distance of the route.

         Returns:
             float: The total distance in kilometers.
         """
        distance = 0
        for i in range(len(self.locations)-1):
            distance += Distance.get_distance(self.locations[i], self.locations[i + 1])
        return distance

    @property
    def estimated_arrival_time(self) -> datetime:
        """
        Gets the estimated arrival time at the final destination.

        Returns:
            datetime: The estimated arrival time.
        """
        return self.stops[self.locations[-1]]

    @property
    def status(self) -> str:
        """
        Gets the current status of the route.

        Returns:
            str: The current status of the route (`STATUS_CREATED`, `STATUS_IN_PROGRESS`, or `STATUS_FINISHED`).
        """
        if ApplicationTime.current() < self.departure_time:
            return self.STATUS_CREATED
        if ApplicationTime.current() > self.estimated_arrival_time:
            return self.STATUS_FINISHED
        else:
            return self.STATUS_IN_PROGRESS

    @property
    def current_location(self) -> str:
        """
        Gets the truck's last known location based on the current time.

        Returns:
            str: The last known location, or the start location if no stops have been reached.
        """
        last_stop = None
        for stop in self.stops:
            if ApplicationTime.current() > self.stops[stop]:
                last_stop = stop
            else:
                break
        return last_stop

    def __str__(self):
        """
        Returns a string representation of the route.

        Returns:
            str: A formatted string containing route details.
        """
        if self.assigned_truck_id:
            truck_info = f"\nAssigned truck ID: {self.assigned_truck_id}"
        else:
            truck_info = ""
        return (
            f"ROUTE DETAILS:"
            f"\nID: {self.id}"
            f"\nHubs:\n{" -> ".join(f"{key}: {value}" for key, value in self.stops.items())}"
            f"\nDeparture time: {self.departure_time.isoformat(sep=" ", timespec="minutes")}"
            f"\nNumber of packages: {len(self._assigned_packages_ids)}"
            f"\nCurrent load: {self.load}"
            f"{truck_info}"
            f"\nStatus: {self.status}"
            f"\nCurrent location: {self.current_location}"
            f"\n" + "=" * 40
        )

    def calculating_estimated_arrival_times(self) -> None:
        """
        Calculates the expected arrival times for each stop along the route.

        Assigns the departure time to the first location in `self.locations`.
        Iterates through each subsequent location, estimating the arrival time based on:
          - The distance between consecutive locations (retrieved via `Location.get_distance`).
          - The average speed defined by `Route.AVERAGE_SPEED`.
        Updates `self._stops` with the computed arrival times, rounded to the nearest minute.

        Uses `replace(second=0, microsecond=0)` to ensure arrival times do not include seconds or microseconds.
        The method does not return anything; it updates `self._stops` in place.
        """
        self._stops[self.locations[0]] = self.departure_time
        estimated_arrival_time = self.departure_time
        for i in range(len(self.locations)-1):
            previous_location = self.locations[i]
            location = self.locations[i+1]

            distance = Distance.get_distance(previous_location, location)
            time_needed = timedelta(hours=distance/Route.AVERAGE_SPEED)
            estimated_arrival_time += time_needed

            self._stops[location] = estimated_arrival_time

    def assign_package(self, package_id: int) -> None:
        """
        Assigns a package to the route.

        Args:
            package_id (int): The ID of the package to assign.
        """
        self._assigned_packages_ids.append(package_id)

    def remove_package(self, package_id: int) -> None:
        """
        Removes a package from the route.

        Args:
            package_id (int): The ID of the package to remove.
        """
        self._assigned_packages_ids.remove(package_id)

    def assign_truck(self, truck_id: int) -> None:
        """
        Assigns a truck to the route.

        Args:
            truck_id (int): The ID of the truck to assign.
        """
        self._assigned_truck_id = truck_id
