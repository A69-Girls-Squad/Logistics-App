from models.package import Package
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

    def is_free(self) -> bool:
        if self._assigned_route == None:
            return True
    
    def assign_to_route(self, route):
        self._assigned_route = route
        self._status = "Assigned"

    def __str__(self):
        return f'Truck with ID: {self._id}, Name: {self.name}, Capacity: {self.capacity}, Range: {self.max_range} created'