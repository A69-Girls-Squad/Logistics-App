import unittest
from unittest.mock import MagicMock
from skeleton.models.truck import Truck

class Truck_Should(unittest.TestCase):

    def test_init(self):
        self.truck_data = {
            "id": 1,
            "name": "Truck A",
            "capacity": 2000,
            "max_range": 5000
        }

        self.truck = Truck.from_json(self.truck_data)

    def test_from_json(self):
        self.assertEqual(self.truck.id, 1)
        self.assertEqual(self.truck.name, "Truck A")
        self.assertEqual(self.truck.capacity, 2000)
        self.assertEqual(self.truck.max_range, 5000)
        self.assertEqual(self.truck.status, Truck.STATUS_FREE)
        self.assertIsNone(self.truck.assigned_route)

    def test_to_json(self):
        pass

    def test_is_free(self):

        route = MagicMock()
        route.dparture_time = 9
        route.Expected_arrival_time = 15
        route.load = 500
        route.distance = 1000


        self.assertTrue(self.truck.is_free(route))
        self.truck.assign_to_route(route)
        self.assertFalse(self.truck.is_free(route))

    def test_assign_to_route(self):
        pass

    def test_remove_from_route(self):
        pass