from datetime import datetime
from networkx.classes import freeze
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
        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        self._location = None
        self._assigned_route_id = None
    
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
            "assigned_route": self._assigned_route_id
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
        
    @property
    def max_range(self):
        return self._max_range
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        self._location = value

    @property
    def assigned_route_id(self):
        return self._assigned_route_id

    def is_suitable(self, route) -> bool:
        """
        Checks if the route is free based on departure time, arrival time, truck capacity and truck max range.
        """
        return (not self.assigned_route_id
                and (self.capacity >= route.load
                and self.max_range >= route.distance))

    def assign_to_route(self, route_id):
        """
        Assigns a truck to a route.
        """
        self._assigned_route_id = route_id
    
    def remove_from_route(self):
        """
        Removes a truck from a route.
        """
        self._assigned_route_id = None

    def status(self) -> str:
        assigned_route = app_data.find_route_by_id(self.assigned_route_id)
        if not self.assigned_route_id or datetime.now() > assigned_route.estimated_arrival_time:
            return Truck.STATUS_FREE
        return Truck.STATUS_BUSY

    def __str__(self):
        return (f"Truck with ID: {self._id}"
                f"\nName: {self.name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range} created"
                f"\nStatus: {app_data.status()}")
