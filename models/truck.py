# Class should have the following attributes:
#
# Id
# Name
# Capacity (kg)
# Max range (km)
# Is free → bool
# Location
#
# Class should have the following methods:
# Dunder str
from models.package import Package
class Truck:
    id_counter = 1001
    def __init__(self, name, capacity, max_range):
        self._id = Truck.id_counter
        Truck.id_counter += 1

        self.name = name
        self.capacity = capacity
        self.max_range = max_range

    @property
    def id(self):
        return self._id

    #def is_free(self, weight) -> bool:
    #    return self.capacity > Package.weight
#
    def __str__(self):
        return f'Truck with ID: {self._id}, Name: {self.name}, Capacity: {self.capacity}, Range: {self.max_range} created'