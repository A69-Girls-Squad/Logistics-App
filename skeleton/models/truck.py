import json
from skeleton.errors.application_error import ApplicationError
class Truck:

    STATUS_FREE = "Free"
    STATUS_BUSY = "Busy"
    _current_id = 1000

    @classmethod
    def next_id(cls) -> int:
        """
         Generates and returns the next unique package ID.

         Returns:
             int: The next unique ID.
         """
        cls._current_id += 1
        return cls._current_id

    def __init__(self, name: str, capacity: int, max_range: int):
        self._id = Truck.next_id()
        if not name.strip():
            raise ApplicationError("Truck name cannot be empty.")
        self._name = name
        self.capacity = capacity
        self.max_range = max_range
        self.status = Truck.STATUS_FREE
        self._location = None
        self._assigned_route = None
    
    @classmethod
    def from_json(cls, data):
        """
        Creates a truck instance from json dictionary.
        """
        return cls(
            name=data["name"],
            capacity=data["capacity"],
            max_range=data["max_range"],
        )
    
    def to_json(self):
        """
        Converts truck instance to a json-compatible dictionary.
        """
        return {
            "id": self._id,
            "name": self.name,
            "capacity": self.capacity,
            "max_range": self.max_range,
            "status": self.status,
            "assigned_route": self._assigned_route
        }

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
        
    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ApplicationError("Truck capacity should be a positive number.")
        self._capacity = value
        
    @property
    def max_range(self):
        return self._max_range
    
    @max_range.setter
    def max_range(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ApplicationError("Truck max range should be a positive number.")
        self._max_range = value
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in [Truck.STATUS_FREE, Truck.STATUS_BUSY]:
            raise ApplicationError("Truck status must be free or busy.")
        self._status = value

    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, new_location):
        self._location = new_location

    @property
    def assigned_route(self):
        return self._assigned_route
    
    def is_free(self, route) -> bool:
        """
        Checks if the route is free based on departure time, arrival time, truck capacity and truck max range.
        """
        return (not self.assigned_route
                or ((self.assigned_route.departure_time > route.expected_arrival_time
                or self.assigned_route.expected_arrival_time < route.departure_time)
                and (self.capacity >= route.load
                and self.max_range >= route.distance)))
    
    def assign_to_route(self, route):
        """
        Assigns a truck to a route.
        Updates truck status.
        """
        self._assigned_route = route
        self._status = Truck.STATUS_BUSY
    
    def remove_from_route(self):
        """
        Removes a truck from a route.
        Updates truck status.
        """
        self._assigned_route = None
        self._status = Truck.STATUS_FREE

    def __str__(self):
        return (f"Truck with ID: {self._id}"
                f"\nName: {self.name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range} created"
                f"\nStatus: {self.status}")
