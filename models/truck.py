import json
class Truck:
    id_counter = 1001
    def __init__(self, name, capacity, max_range):
        self._id = Truck.id_counter
        Truck.id_counter += 1

        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        self._assigned_route = None
        self._status = "Free"
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

    def is_free(self) -> bool:
        if self._assigned_route == None:
            return True
    
    def assign_to_route(self, route):
        self._assigned_route = route
        self._status = "Busy"
    
    def remove_from_route(self):
        self._assigned_route = None
        self._status = "Free"

    def __str__(self):
        return f'Truck with ID: {self._id}, Name: {self.name}, Capacity: {self.capacity}, Range: {self.max_range} created'