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
        self._assigned_route_id = None

    @classmethod
    def from_json(cls, data):
        """
        Creates a Truck instance from a JSON dictionary.

        Args:
            data (dict): A dictionary containing truck details, including:
                - id (int): The truck's unique identifier.
                - name (str): The name of the truck.
                - capacity (int): The capacity of the truck.
                - max_range (int): The maximum range of the truck.
                - assigned_route_id (int or None): The ID of the assigned route.

        Returns:
            Truck: An instance of the Truck class.
        """
        truck = cls(
            name=data["name"],
            capacity=data["capacity"],
            max_range=data["max_range"]
        )
        truck._id = data["id"]
        truck._assigned_route_id = data["assigned_route_id"]

        return truck

    def to_json(self) -> dict:
        """
        Converts the Truck instance into a JSON dictionary.

        Returns:
            dict: A dictionary representation of the truck, including:
                - id (int): The truck's unique identifier.
                - name (str): The name of the truck.
                - capacity (int): The capacity of the truck.
                - max_range (int): The maximum range of the truck.
                - assigned_route_id (int or None): The ID of the assigned route.
        """
        return {
            "id": self._id,
            "name": self._name,
            "capacity": self._capacity,
            "max_range": self._max_range,
            "assigned_route_id": self._assigned_route_id
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
    def assigned_route_id(self):
        return self._assigned_route_id

    @assigned_route_id.setter
    def assigned_route_id(self, value):
        self._assigned_route_id = value

    def is_suitable(self, route) -> bool:
        """
        Checks if the route is free based on departure time, arrival time, truck capacity and truck max range.
        """
        return (not self.assigned_route_id
                and (self.capacity >= route.load
                and self.max_range >= route.distance))

    def __str__(self):
        if self._assigned_route_id:
            truck_status = (f"Busy"
                            f"\nRoute ID: {self._assigned_route_id}")
        else:
            truck_status = "Free"

        return (f"Truck with ID: {self._id}"
                f"\nName: {self._name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range} created"
                f"\nStatus: {truck_status}")