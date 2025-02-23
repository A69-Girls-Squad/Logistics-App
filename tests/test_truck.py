import unittest
from unittest.mock import MagicMock
from models.truck import Truck

class TestTruck(unittest.TestCase):

    def setUp(self):
        Truck._current_id = 1000

    def test_next_id(self):
        first_id = Truck.next_id()
        second_id = Truck.next_id()
        
        self.assertEqual(first_id, 1001)
        self.assertEqual(second_id, 1002)

    def test_truck_init(self):
        truck = Truck(name="Truck1", capacity=1000, max_range=5000)
        
        self.assertEqual(truck._name, "Truck1")
        self.assertEqual(truck._capacity, 1000)
        self.assertEqual(truck._max_range, 5000)
        self.assertEqual(truck.id, 1001)
        self.assertIsNone(truck._assigned_route_id)

    def test_from_json(self):
        data = {
            "id": 1001,
            "name": "Truck1",
            "capacity": 1000,
            "max_range": 5000,
            "assigned_route_id": None
        }
        
        truck = Truck.from_json(data)
        
        self.assertEqual(truck.id, 1001)
        self.assertEqual(truck._name, "Truck1")
        self.assertEqual(truck._capacity, 1000)
        self.assertEqual(truck._max_range, 5000)
        self.assertIsNone(truck._assigned_route_id)

    def test_to_json(self):
        truck = Truck(name="Truck1", capacity=1000, max_range=5000)
        expected_json = {
            "id": 1001,
            "name": "Truck1",
            "capacity": 1000,
            "max_range": 5000,
            "assigned_route_id": None
        }
        
        self.assertEqual(truck.to_json(), expected_json)

    def test_is_suitable(self):
        route = MagicMock()
        route.load = 5000
        route.distance = 4000
        truck = Truck(name="Truck1", capacity=10000, max_range=6000)
        
        self.assertTrue(truck.is_suitable(route))

    def test_is_suitable_unsufficient_capacity(self):
        route = MagicMock()
        route.load = 5000
        route.distance = 4000
        truck = Truck(name="Truck1", capacity=1000, max_range=6000)
        
        self.assertFalse(truck.is_suitable(route))

    def test_is_suitable_unsufficient_max_range(self):
        route = MagicMock()
        route.load = 5000
        route.distance = 4000
        truck = Truck(name="Truck1", capacity=10000, max_range=2000)
        
        self.assertFalse(truck.is_suitable(route))

    def test_is_suitable_truck_is_busy(self):
        route = MagicMock()
        route.load = 5000
        route.distance = 4000
        
        truck = Truck(name="TestTruck", capacity=10000, max_range=6000)
        truck.assigned_route_id = 1
        
        self.assertFalse(truck.is_suitable(route))

    def test_str_method(self):
        truck = Truck(name="Truck1", capacity=1000, max_range=5000)
        expected_str = (
            f"Truck with ID: 1001\n"
            f"Name: Truck1\n"
            f"Capacity: 1000\n"
            f"Range: 5000 created\n"
            f"Status: Free"
        )
        
        self.assertEqual(str(truck), expected_str)

        truck._assigned_route_id = 1
        expected_str_busy = (
            f"Truck with ID: 1001\n"
            f"Name: Truck1\n"
            f"Capacity: 1000\n"
            f"Range: 5000 created\n"
            f"Status: Busy\nRoute ID: 1"
        )
        
        self.assertEqual(str(truck), expected_str_busy)