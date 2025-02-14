import datetime
import uuid
from models.location import Location
from models.package import Package
from models.truck import Truck


class Route:

    AVERAGE_SPEED = 87

    '''
    Defines the possible statuses of a route during its lifecycle:
    
    1. **Created** - Assigned to a route after creation but before departure.
    2. **In progress** - The route is in progress between departure and the estimated arrival time at the final location.
    3. **Finished** - The route has reached its final destination after the estimated arrival time.
    '''
    STATUS_CREATED = "Created"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_FINISHED = "Finished"

    def __init__(self, locations: list[str], departure_time: str):
        self.locations = locations
        self.departure_time = departure_time

        self._id = uuid.uuid1().hex[:6]
        self._assigned_truck = None
        self._assigned_packages = []
        self._load = 0
        self._stops = {}
        self.calculating_expected_arrival_times()

    '''
    Manages the locations where the route will stop.

    The user provides a string containing a list of locations, separated by commas. 
    Upon initialization, this string is converted into a list of individual location names.

    - The **locations** property returns the locations as a tuple.
    - The setter validates the input, ensuring:
      1. Locations exist in the predefined `Location.CITIES` list.
      2. At least two locations are provided.
      3. Locations are correctly separated by commas.

    Raises:
        ValueError:
        - If locations are not separated by comma.
        - If an invalid location is provided.
        - If fewer than two locations are specified.
    '''
    @property
    def locations(self):
        return tuple(self._locations)

    @locations.setter
    def locations(self, value: str):
        try:
            if ',' not in value:
                raise ValueError(f"Locations should be separated by ','")
            value = value.split(",")

            for location in value:
                if location not in Location.CITIES:
                    raise ValueError(f"Invalid location: {location}.")

            if len(value) < 2:
                raise ValueError("Too few locations!")

        except ValueError as v:
            print(v.args[0])

        self._locations = value

    '''
    The user inputs a string representing the departure time of the route in the following format: dd/mm/YYYY-HH:MM.
    At initialization the string is converted to datetime object.
    '''
    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: str):
        if datetime.datetime.strptime(value, '%d/%m/%Y-%H:%M') < datetime.datetime.now():
            raise ValueError("Invalid time!")
        self._departure_time = datetime.datetime.strptime(value, '%d/%m/%Y-%H:%M')

    '''
    At initialization the route gets a uuid.
    '''
    @property
    def id(self):
        return self._id

    '''
    At initialization the attribute of the assigned truck gets a None value.
    Later the user can assign a truck object to the route but only if the truck is free for the time 
    from the departure until the estimated arrival time of the route. 
    '''
    @property
    def assigned_truck(self):
        return self._assigned_truck

    @assigned_truck.setter
    def assigned_truck(self, value: Truck):
        if not value.is_free:
            raise ValueError("This truck is not free!")
        self._assigned_truck = value

    '''
    At initialization an empty list of assigned packages is created which is to be used to assign packages to the route
    with the assign_package_tou_route command.
    '''
    @property
    def assigned_packages(self):
        return tuple(self._assigned_packages)

    '''
    The load attribute is incremented with the amount of the package's weight at the moment of assignment.
    '''
    @property
    def load(self):
        return self._load

    @property
    def stops(self):
        return self._stops

    @property
    def free_capacity(self):
        if not self.assigned_truck:
            raise AttributeError("No truck assigned yet!")
        return self.assigned_truck.capacity - self.load

    @property
    def distance(self):
        distance = 0
        for i in range(len(self.locations)-1):
            distance += Location.get_distance(self.locations[i], self.locations[i + 1])
        return distance

    @property
    def expected_arrival_time(self):
        return self._stops[-1]

    @property
    def status(self):
        if datetime.datetime.now() < self.departure_time:
            return self.STATUS_CREATED
        if datetime.datetime.now() > self.expected_arrival_time:
            return self.STATUS_FINISHED
        else:
            return self.STATUS_IN_PROGRESS

    @property
    def current_location(self):
        for stop in self.stops:
            if datetime.datetime.now() > self.stops[stop]:
                return stop

    def __str__(self):
        return (
            f"Route Details:"
            f"\nID: {self.id}"
            f"\nHubs:\n{' -> '.join(f'{key}: {value}' for key, value in self.stops.items())}"
            f"\nDeparture Time: {self.departure_time.strftime("%d/%m/%Y %H:%M")}"
            f"\nNumber of Packages: {len(self.assigned_packages)}"
            f"\nCurrent Load: {self.load}"
            f"\nAssigned Truck ID: {self.assigned_truck.id}"
            f"\nStatus: {self.status}"
            f"\nCurrent Location: {self.current_location}"
            f"\n============"
        )

    def calculating_expected_arrival_times(self):              # stops: {SYD: 16/02, MEL: 17/02, BRI: 19/02}
        self._stops[self.locations[0]] = self.departure_time
        expected_arrival_time = self.departure_time
        for i in range(1, len(self.locations)):
            previous_location = self.locations[i-1]
            location = self.locations[i]
            distance = Location.get_distance(previous_location, location)
            time_needed = datetime.timedelta(hours=distance/Route.AVERAGE_SPEED)
            expected_arrival_time += time_needed
            self._stops[location] = expected_arrival_time.replace(second=0, microsecond=0)

    def assign_truck(self, truck: Truck):
        self.assigned_truck = truck

    def remove_truck(self):
        self.assigned_truck = None
        

    def assign_package(self, package: Package):
        self._assigned_packages.append(package)
        self._load += package.weight
        package.assigned_route = self