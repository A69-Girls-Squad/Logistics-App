import datetime
import json
import os
import uuid

from skeleton.errors.application_error import ApplicationError
from skeleton.models.package import Package
from skeleton.models.truck import Truck


class Route:

    CITIES = [
        "SYD",
        "MEL",
        "ADL",
        "ASP",
        "BRI",
        "DAR",
        "PER",
    ]

    AVERAGE_SPEED = 87

    LOCATIONS_SEPARATOR = ","
    REQUIRED_DATE_FORMAT = "%d/%m/%Y-%H:%M"
    REQUIRED_DATE_FORMAT_STRING = "dd/mm/YYYY-HH:MM"

    """
    Defines the possible statuses of a route during its lifecycle:
    
    1. **Created** - Assigned to a route after creation but before departure.
    2. **In progress** - The route is in progress between departure and the estimated arrival time at the final location.
    3. **Finished** - The route has reached its final destination after the estimated arrival time.
    """
    STATUS_CREATED = "Created"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_FINISHED = "Finished"

    def __init__(self, locations: str, departure_time: str):        # SYD: 16/02, MEL: 17/02, BRI:19/02
        self.locations = locations
        self.departure_time = departure_time

        self._id = uuid.uuid1().hex[:6]
        self._assigned_truck = None    # Removed TypeHint `:Truck` because at init no truck is assigned
        self._assigned_packages = []
        self._load = 0
        self._stops = {}
        if isinstance(self.locations, list):
            self.calculating_estimated_arrival_times()

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
        try:
            if not isinstance(value, str):
                raise ApplicationError("Error")
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

        except ValueError as v:
            print(v.args[0])

        except ApplicationError as ap:
            print(ap.args[0])

        finally:
            self._locations = value

    """
    Gets and sets the departure time of the route.

    The user provides a string representing the departure time in the format: "dd/mm/YYYY-HH:MM".  
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
            formatted_date = datetime.datetime.strptime(value, self.REQUIRED_DATE_FORMAT)
            if formatted_date < datetime.datetime.now():
                raise ApplicationError("Departure time must be in the future!")
            self._departure_time = datetime.datetime.strptime(value, self.REQUIRED_DATE_FORMAT)

        except ValueError:
            print(f"Departure time {value} does not match the format {self.REQUIRED_DATE_FORMAT_STRING}")

        except ApplicationError as ap:
            print(ap.args[0])

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
    def assigned_truck(self):
        return self._assigned_truck

    @assigned_truck.setter #Unnecessary to have setter. We have assign_truck method. Should do validations there
    def assigned_truck(self, value: Truck):
        try:
            if not isinstance(value, Truck):
                raise ApplicationError("Invalid truck!")
            if not value.status == Truck.STATUS_FREE:
                raise ApplicationError("This truck is not free!")
            self._assigned_truck = value

        except ApplicationError as ae:
            print(ae.args[0])

    """
    Manages the packages assigned to the route.
    
    At initialization, an empty list is created to store assigned packages.  
    Packages can be added to the route using the `assign_package_to_route` method.
    
    Returns:
        tuple: A tuple containing all assigned packages.
    """
    @property
    def assigned_packages(self):
        return tuple(self._assigned_packages)

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
        self.calculating_estimated_arrival_times()
        return self._stops

    """
    Calculates the remaining free capacity of the assigned truck.

    This value is determined by subtracting the total weight of all assigned packages (`load`)  
    from the truck"s capacity.

    Raises:
        AttributeError: If no truck has been assigned to the route.

    Returns:
        float: The remaining capacity of the assigned truck.
    """
    @property
    def free_capacity(self):
        try:
            if not self.assigned_truck:
                raise ApplicationError("No truck assigned yet!")
            return self.assigned_truck.capacity - self.load
        except ApplicationError as ae:
            print(ae.args[0])

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
            distance += Route.get_distance(self.locations[i], self.locations[i + 1])
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
        if datetime.datetime.now() < self.departure_time:
            return self.STATUS_CREATED
        if datetime.datetime.now() > self.estimated_arrival_time:
            return self.STATUS_FINISHED
        else:
            return self.STATUS_IN_PROGRESS

    """
    Returns the truck"s estimated last known location based on the current time.
    If no stops have been reached yet, the start location is returned by default
    """
    @property
    def current_location(self):    # To be tested further - not sure if it works correctly
        last_stop = None
        for stop in self.stops:
            if datetime.datetime.now() > self.stops[stop]:
                last_stop = stop
            else:
                break
        return last_stop

    @staticmethod
    def get_distance(city_1, city_2):
        """
        Retrieves the distance between two cities from a pre-defined JSON file.

        Parameters:
        - `city_1` (str): The name of the starting city.
        - `city_2` (str): The name of the destination city.

        Returns:
        - `float | int`: The distance between `city_1` and `city_2` as stored in the JSON file.

        Loads distance data from `json/distances.json`.
        Extracts the distance value using the provided city names.
        """
        try:
            if city_1 not in Route.CITIES:
                raise ApplicationError(f"Invalid city: {city_1}")
            if city_2 not in Route.CITIES:
                raise ApplicationError(f"Invalid city: {city_2}")
            if city_1 == city_2:
                raise ApplicationError("Cities cannot be the same!")

            file_path = os.path.join(os.path.dirname(__file__), "json/distances.json")

            with open(file_path, "r") as distances:
                distance_data = json.loads(distances.read())
            return distance_data[city_1][0][city_2]

        except ApplicationError as ae:
            print(ae.args[0])

    def __str__(self):
        if self.assigned_truck:
            truck_info = f"\nAssigned Truck ID: {self.assigned_truck.id}"
        else:
            truck_info = ""
        return (
            f"Route Details:"
            f"\nID: {self.id}"
            f"\nHubs:\n{" -> ".join(f"{key}: {value}" for key, value in self.stops.items())}"
            f"\nDeparture Time: {self.departure_time.strftime("%d/%m/%Y %H:%M")}"
            f"\nNumber of Packages: {len(self.assigned_packages)}"
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
        for i in range(len(self.locations)):
            previous_location = self.locations[i-1]
            location = self.locations[i]

            distance = Route.get_distance(previous_location, location)
            time_needed = datetime.timedelta(hours=distance/Route.AVERAGE_SPEED)
            estimated_arrival_time += time_needed

            self._stops[location] = estimated_arrival_time.replace(second=0, microsecond=0)

    def assign_truck(self, truck: Truck):
        """
        Assigns a truck to the route.

        Associates the provided `truck` object with the route.
        The assignment process is validated through the setter method.
        """
        self.assigned_truck = truck
        # Add is_assigned to Truck so it is like Package, to know if the truck is assigned or not and check here

    def remove_truck(self):
        """
        Removes the currently assigned truck from the route.
        If no truck is currently assigned, the method simply ensures `self.assigned_truck` remains `None`.
        """
        self.assigned_truck = None
        try:
            if not self.assigned_truck:
                raise ApplicationError("No truck assigned to this route!")
            self.assigned_truck = None

        except ApplicationError as ae:
            print(ae.args[0])

    def assign_package(self, package: Package):
        """
        Assigns a package to the route and updates relevant attributes.

        Adds the given `package` to the list of assigned packages.
        Increases the total route load by the package"s weight.
        Links the package to this route by updating its `assigned_route` attribute.
        """
        try:
            if not isinstance(package, Package):
                raise ApplicationError("Invalid package")
            if package in self._assigned_packages:
                raise ApplicationError(f"Package with ID {package.id} already assigned to Route with ID {self._id}")
            if self.assigned_truck and self.free_capacity < package.weight:
                raise ApplicationError("No more capacity")
            self._assigned_packages.append(package)
            self._load += package.weight
            package.route = self

        except ApplicationError as ae:
            print(ae.args[0])