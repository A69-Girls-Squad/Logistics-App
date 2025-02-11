import json
class Truck:

    STATUS_FREE = "Free"
    STATUS_BUSY = "Busy"

    def __init__(self, name: str, capacity: int, max_range: int):
        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        self._assigned_route = None
        self._status = Truck.STATUS_FREE
        self._location = None
    
    @classmethod
    def from_json(cls, data):
        return cls(
            truck_id=data["id"],
            name=data["name"],
            capacity=data["capacity"],
            max_range=data["max_range"],
        )
    
    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "capacity": self._capacity,
            "max_range": self._max_range,
            "status": self._status,
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
    
    @property
    def max_range(self):
        return self._max_range
    
    @property
    def status(self):
        return self._status
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, new_location):
        self._location = new_location

    # property for assigned_route

    def is_free(self, route) -> bool:
        return (not self.assigned_route
                or ((self.assigned_route.departure_time > route.expected_arrival_time
                or self.assigned_route.expected_arrival_time < route.departure_time)
                and (self.capacity >= route.load
                and self.max_range >= route.distance)))
    
    def assign_to_route(self, route):
        self._assigned_route = route
        self._status = Truck.STATUS_BUSY
    
    def remove_from_route(self):
        self._assigned_route = None
        self._status = Truck.STATUS_FREE

    def __str__(self):
        return (f"Truck with ID: {self._id}"
                f"\nName: {self.name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range} created"
                f"\nStatus: {self.status}")