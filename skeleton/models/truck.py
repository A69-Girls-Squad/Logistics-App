

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

    @classmethod
    def from_json(cls, data):

        truck = cls(
            name=data["name"],
            capacity=data["capacity"],
            max_range=data["max_range"]
        )
        truck._id = data["id"]
        truck._location = data["location"]
        truck._assigned_route_id = data["assigned_route_id"]

        return truck

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "capacity": self._capacity,
            "max_range": self._max_range,
            "location": self._location,
            "assigned_route_id": self._assigned_route_id
        }

    def __init__(self, name: str, capacity: int, max_range: int):
        self._id = Truck.next_id()
        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        self._location = None
        self._assigned_route_id = None

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


    def __str__(self):
        if self._assigned_route_id:
            truck_status = (f"Busy"
                            f"\nRoute ID: {self._assigned_route_id}")
        else:
            truck_status = "Free"

        return (f"Truck with ID: {self._id}"
                f"\nName: {self.name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range} created"
                f"\nStatus: {truck_status}")
