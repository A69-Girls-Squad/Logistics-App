import datetime
from models.location import Location
from models.package import Package
from models.truck import Truck


class Route:

    AVERAGE_SPEED = 87
    STATUS_CREATED = "Created"
    STATUS_IN_PROGRESS = "In progress"
    STATUS_FINISHED = "Finished"

    def __init__(self, id, locations: list[Location], departure_time: datetime):
        self._id = id    # To implement automatic generation
        self.locations = locations
        self.departure_time = departure_time
        self._assigned_truck = None
        self._assigned_packages = []
        self._load = 0
        self._stops = {}

    @property
    def id(self):
        return self._id

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, value: list[Location]):
        if len(value) < 2:
            raise AttributeError("Too few locations!")
        self._locations = value

    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: datetime):
        if value < datetime.now():
            raise ValueError("Invalid time!")
        self._departure_time = value

    @property
    def assigned_truck(self):
        return self._assigned_truck

    @assigned_truck.setter
    def assigned_truck(self, value: Truck):
        if not value.is_free:
            raise ValueError("This truck is not free!")
        self._assigned_truck = value

    @property
    def assigned_packages(self):
        return tuple(self._assigned_packages)

    @property
    def load(self):
        return self._load

    @property
    def free_capacity(self):
        if not self.assigned_truck:
            raise AttributeError("No truck assigned yet!")
        return self.assigned_truck.capacity - self.load

    @property
    def distance(self):
        distance = 0
        for i in range(len(self.locations) - 1):
            distance += Location.get_distance(self.locations[i], self.locations[i + 1])
        return distance

    @property
    def expected_arrival_time(self):
        return self._stops[-1]

    @property
    def status(self):
        if datetime.now() < self.departure_time:
            return self.STATUS_CREATED
        if datetime.now() > self.expected_arrival_time:
            return self.STATUS_FINISHED
        else:
            return self.STATUS_IN_PROGRESS

    def __str__(self):
        locations = [location.name for location in self.locations]
        return (
            f"Route Details:\nHubs: {" -> ".join(locations)}"
            f"\nDeparture Time: {self.departure_time.strftime("%m/%d %Y%H:%M")}"
            f"\nCurrent Load: {self.load}"
            f"\nAssigned Truck ID: {self.assigned_truck.id}"
        )

    def calculating_expected_arrival_times(self):
        expected_arrival_time = self.departure_time
        for i in range(1, len(self.locations)):
            previous_location = self.locations[i-1]
            location = self.locations[i]
            distance = location.get_distance(previous_location, location)
            time_needed = datetime.timedelta(hours=distance/Route.AVERAGE_SPEED)
            expected_arrival_time += time_needed
            self._stops[location] = expected_arrival_time