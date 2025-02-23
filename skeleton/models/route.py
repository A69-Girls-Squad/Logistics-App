from datetime import datetime, timedelta

from core.application_time import ApplicationTime
from errors.application_error import ApplicationError
from models.truck import Truck
from models.constants.distances import Distance


class Route:

    CITIES = list(Distance.DISTANCES)
    AVERAGE_SPEED = 87
    LOCATIONS_SEPARATOR = ","
    REQUIRED_DATE_FORMAT = '%Y-%m-%d %H:%M'

    """
    Defines the possible statuses of a route during its lifecycle:
    
    1. **Created** - Assigned to a route after creation but before departure.
    2. **In progress** - The route is in progress between departure and the estimated arrival time at the final location.
    3. **Finished** - The route has reached its final destination after the estimated arrival time.
    """
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
        # stops_data = data.get("stops", {})
        # route._stops = {loc: datetime.fromisoformat(time) if time else None
        #                 for loc, time in stops_data.items()}


        return route

    def to_json(self) -> dict:
        """
        Converts the Route object into a JSON dictionary.

        Returns:
            dict: A dictionary representation of the route, including:
                - locations (str): The locations string.
                - departure_time (str): The departure time in REQUIRED_DATE_FORMAT.
                - _id (str): The route's unique identifier.
                - _assigned_truck_id (int or None): The ID of the assigned truck.
                - _assigned_package_ids (list): The list of assigned package IDs.
                - _load (float): The total load weight.
                - _stops (dict): A dictionary mapping locations to estimated arrival times (as ISO strings).
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

    """
    Manages the locations where the route will stop.

    The user provides a string containing a list of locations, separated by commas. 
    Upon initialization, this string is converted into a list of individual location names.

    - The **locations** property returns the locations as a tuple.
    - The setter validates the input, ensuring:
      1. Locations exist in the predefined `Location.CITIES` list.
      2. At least two locations are provided.
      3. Locations are correctly separated by commas.

    Raises:
        ApplicationError:
        - If locations are not separated by the expected delimiter.
        - If one or more provided locations are not found in `Location.CITIES`.
        - If the list contains fewer than two locations.
        - If consecutive duplicate locations are detected.
    """
    @property
    def locations(self):
        return tuple(self._locations)

    @locations.setter
    def locations(self, value: str):

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

    """
    Gets and sets the departure time of the route.

    The user provides a string representing the departure time in the format: "dd/mm/YYYY HH:MM".  
    Upon setting, the string is converted into a `datetime` object.  
    If the provided time is in the past, a `ValueError` is raised.  
    
    Returns:
        datetime.datetime: The departure time as a `datetime` object.
    
    Raises:
        ApplicationError:
        - If the provided string is not in the requested format.
        - If the provided departure time is in the past.
    """
    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: str):
        try:
            departure_time = datetime.fromisoformat(value)
            if departure_time < ApplicationTime.current():
                raise ApplicationError("Departure time must be in the future!")
            self._departure_time = departure_time

        except ValueError:
            raise ApplicationError(f"Departure time {value} "
                                   f"does not match the format {self.REQUIRED_DATE_FORMAT}")


    """
    Returns the unique identifier (UUID) of the route.

    Each route is assigned a UUID upon initialization to ensure uniqueness.

    Returns:
        str: The unique identifier of the route.
    """
    @property
    def id(self):
        return self._id

    """
    Manages the truck assigned to the route.
    
    At initialization, the `assigned_truck` attribute is set to `None`.  
    Later, a truck object can be assigned to the route, but only if it is available  
    for the entire duration of the route, from departure to estimated arrival.
    
    Raises:
        ValueError: If the truck is not free at the time of assignment.
    
    Returns:
        Truck | None: The currently assigned truck or `None` if no truck has been assigned.
    """
    @property
    def assigned_truck_id(self):
        return self._assigned_truck_id

    @assigned_truck_id.setter
    def assigned_truck_id(self, value: Truck):
        self._assigned_truck_id = value

    """
    Manages the packages assigned to the route.
    
    At initialization, an empty list is created to store assigned packages.  
    Packages can be added to the route using the `assign_package_to_route` method.
    
    Returns:
        tuple: A tuple containing all assigned packages.
    """
    @property
    def assigned_packages_ids(self):
        return tuple(self._assigned_packages_ids)

    """
    Represents the total load weight of the route.
    
    The `load` attribute increases by the weight of each package when assigned to the route.  
    This helps track the total weight of all assigned packages.
    
    Returns:
        float: The current total load weight of the route.
    """
    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, value: int):
        self._load = value

    """
    Represents the estimated arrival times for each stop along the route.
    
    This attribute converts the `locations` list into a dictionary,  where:
    - the keys are location names
    - the values are their estimated arrival times.
    
    Before returning the dictionary, the method calculates the estimated arrival times  
    by calling `calculating_expected_arrival_times()`.
    
    Returns:
        dict: A dictionary mapping location names (str) to estimated arrival times (datetime).
    """
    @property
    def stops(self):
        return self._stops

    """
    Calculates the total distance of the route.

    The total distance is computed by summing the distances between consecutive locations  
    along the route, representing the entire journey the truck will travel.

    Returns:
        float: The total distance of the route in kilometers.
    """
    @property
    def distance(self):
        distance = 0
        for i in range(len(self.locations)-1):
            distance += Distance.get_distance(self.locations[i], self.locations[i + 1])
        return distance

    """
    Gets the estimated arrival time of the truck at the final destination.

    The arrival time is determined based on the calculated stop times along the route.

    Returns:
        datetime: The estimated arrival time at the last stop.
    """
    @property
    def estimated_arrival_time(self):
        return self.stops[self.locations[-1]]

    """
    Determines the current status of the route based on the current time.

    The status can be one of the following:  
    - `STATUS_CREATED`: The route has not yet departed.  
    - `STATUS_IN_PROGRESS`: The route is currently ongoing.  
    - `STATUS_FINISHED`: The route has been completed.

    Returns:
        str: The current status of the route.
    """
    @property
    def status(self):
        if ApplicationTime.current() < self.departure_time:
            return self.STATUS_CREATED
        if ApplicationTime.current() > self.estimated_arrival_time:
            return self.STATUS_FINISHED
        else:
            return self.STATUS_IN_PROGRESS

    """
    Returns the truck"s estimated last known location based on the current time.
    If no stops have been reached yet, the start location is returned by default
    """
    @property
    def current_location(self):
        last_stop = None
        for stop in self.stops:
            if ApplicationTime.current() > self.stops[stop]:
                last_stop = stop
            else:
                break
        return last_stop

    def __str__(self):
        if self.assigned_truck_id:
            truck_info = f"\nAssigned Truck ID: {self.assigned_truck_id}"
        else:
            truck_info = ""
        return (
            f"Route Details:"
            f"\nID: {self.id}"
            f"\nHubs:\n{" -> ".join(f"{key}: {value.isoformat(sep=" ", timespec="minutes")}" for key, value in self.stops.items())}"
            f"\nDeparture Time: {self.departure_time.isoformat(sep=" ", timespec="minutes")}"
            f"\nNumber of Packages: {len(self._assigned_packages_ids)}"
            f"\nCurrent Load: {self.load}"
            f"{truck_info}"
            f"\nStatus: {self.status}"
            f"\nCurrent Location: {self.current_location}"
            f"\n============"
        )

    def calculating_estimated_arrival_times(self):
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

    def assign_package(self, package_id):
        self._assigned_packages_ids.append(package_id)

    def remove_package(self, package_id):
        self._assigned_packages_ids.remove(package_id)

    def assign_truck(self, truck_id):
        self._assigned_truck_id = truck_id
