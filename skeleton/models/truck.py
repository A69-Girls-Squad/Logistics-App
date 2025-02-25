class Truck:
    """Represents a delivery truck.

    A Truck has a unique ID, a name, capacity, and a maximum range.
    It can be assigned to a specific route, and its status changes accordingly.

    Attributes:
        STATUS_FREE (str): Status when the truck is available.
        STATUS_BUSY (str): Status when the truck is assigned to a route.
        _current_id (int): Class-level counter for generating unique truck IDs.
    """

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
        """Initialize a Truck instance.

        Args:
            name (str): The name of the truck.
            capacity (int): The maximum load capacity of the truck.
            max_range (int): The maximum travel distance of the truck.
        """
        self._id = Truck.next_id()
        self._name = name
        self._capacity = capacity
        self._max_range = max_range
        self._assigned_route_id = None

    @classmethod
    def from_json(cls, data):
        """Create a Truck instance from a dictionary.

        Args:
            data (dict): Truck details including ID, name, capacity, max range, and assigned route.

        Returns:
            Truck: A new Truck instance.
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
        """Convert the Truck instance into a dictionary.

        Returns:
            dict: A dictionary representation of the truck.
        """
        return {
            "id": self._id,
            "name": self._name,
            "capacity": self._capacity,
            "max_range": self._max_range,
            "assigned_route_id": self._assigned_route_id
        }

    @property
    def id(self) -> int:
        """Get the truck's unique ID.

        Returns:
            int: The truck's ID.
        """
        return self._id

    @property
    def name(self) -> str:
        """Get the truck's name.

        Returns:
            str: The name of the truck.
        """
        return self._name
        
    @property
    def capacity(self) -> int:
        """Get the truck's capacity.

        Returns:
            int: The truck's maximum load capacity.
        """
        return self._capacity
        
    @property
    def max_range(self) -> int:
        """Get the truck's maximum range.

        Returns:
            int: The truck's maximum travel distance.
        """
        return self._max_range

    @property
    def assigned_route_id(self) -> int:
        """Get the assigned route ID.

        Returns:
            int: The ID of the assigned route, or None if the truck is free.
        """
        return self._assigned_route_id

    @assigned_route_id.setter
    def assigned_route_id(self, value) -> None:
        """Set the assigned route ID.

        Args:
            value (int): The route ID to assign to the truck.
        """
        self._assigned_route_id = value

    def is_suitable(self, route) -> bool:
        """
        Checks if the route is free based on departure time, arrival time, truck capacity and truck max range.
        """
        return (not self.assigned_route_id
                and (self.capacity >= route.load
                and self.max_range >= route.distance))

    def __str__(self):
        """Return a string representation of the truck.

        Returns:
            str: Formatted truck details.
        """
        if self._assigned_route_id:
            truck_status = (f"Busy"
                            f"\nRoute ID: {self._assigned_route_id}")
        else:
            truck_status = "Free"

        return (f"TRUCK DETAILS:"
                f"\nID: {self._id}"
                f"\nName: {self._name}"
                f"\nCapacity: {self.capacity}"
                f"\nRange: {self.max_range}"
                f"\nStatus: {truck_status}")