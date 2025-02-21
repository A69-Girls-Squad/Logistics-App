import unittest
from unittest.mock import MagicMock
from models.truck import Truck
from errors.application_error import ApplicationError

class Truck_Should(unittest.TestCase):

    def test_init(self):
        self.truck_data = {
            "id": 1,
            "name": "Truck Scania",
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

    def test_to_json(self): # TO DO 
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

        route = MagicMock()
        route.dparture_time = 9
        route.Expected_arrival_time = 15
        route.load = 500
        route.distance = 1000

        self.truck.assign_to_route(route)

        self.assertEqual(self.truck.status, Truck.STATUS_BUSY)
        self.assertEqual(self.truck.assign_to_route, route)

    def test_remove_from_route(self):
        route = MagicMock()
        route.dparture_time = 9
        route.Expected_arrival_time = 15
        route.load = 500
        route.distance = 1000

        self.truck.assign_to_route(route)

        self.assertEqual(self.truck.status, Truck.STATUS_FREE)
        self.assertEqual(self.truck.assign_to_route, route)

    def test_invalid_name(self):
        with self.assertRaises(ApplicationError):
            Truck(1001, "", 5000, 6000)

    def test_invalid_capacity(self):
        with self.assertRaises(ApplicationError):
            Truck(1001, "Scania", -5000, 6000)

    def test_invalid_max_range(self):
        with self.assertRaises(ApplicationError):
            Truck(1001, "", 5000, -6000)
