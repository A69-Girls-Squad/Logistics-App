import unittest
from unittest.mock import MagicMock
import test_data as td
from models.truck import Truck


class Truck_Should(unittest.TestCase):

    def setUp(self):
        Truck._current_id = 1000  # Reset ID counter before each test

    def test_next_id(self):
        first_id = Truck.next_id()
        second_id = Truck.next_id()

        self.assertEqual(first_id, 1001)
        self.assertEqual(second_id, 1002)

    def test_truck_init(self):
        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)

        self.assertEqual(truck.name, td.VALID_TRUCK_NAME)
        self.assertEqual(truck.capacity, td.VALID_TRUCK_CAPACITY)
        self.assertEqual(truck.max_range, td.VALID_TRUCK_MAX_RANGE)
        self.assertEqual(truck.id, 1001)
        self.assertIsNone(truck.assigned_route_id)

    def test_from_json(self):
        data = {
            "id": 1001,
            "name": td.VALID_TRUCK_NAME,
            "capacity": td.VALID_TRUCK_CAPACITY,
            "max_range": td.VALID_TRUCK_MAX_RANGE,
            "assigned_route_id": None
        }

        truck = Truck.from_json(data)

        self.assertEqual(truck.id, 1001)
        self.assertEqual(truck.name, td.VALID_TRUCK_NAME)
        self.assertEqual(truck.capacity, td.VALID_TRUCK_CAPACITY)
        self.assertEqual(truck.max_range, td.VALID_TRUCK_MAX_RANGE)
        self.assertIsNone(truck.assigned_route_id)

    def test_to_json(self):
        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)
        expected_json = {
            "id": 1001,
            "name": td.VALID_TRUCK_NAME,
            "capacity": td.VALID_TRUCK_CAPACITY,
            "max_range": td.VALID_TRUCK_MAX_RANGE,
            "assigned_route_id": None
        }

        self.assertEqual(truck.to_json(), expected_json)

    def test_is_suitable(self):
        route = MagicMock()
        route.load = td.VALID_TRUCK_CAPACITY - 1000  # Within capacity
        route.distance = td.VALID_TRUCK_MAX_RANGE - 1000  # Within max range

        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)

        self.assertTrue(truck.is_suitable(route))

    def test_is_suitable_insufficient_capacity(self):
        route = MagicMock()
        route.load = td.VALID_TRUCK_CAPACITY + 1000  # Exceeds capacity
        route.distance = td.VALID_TRUCK_MAX_RANGE - 1000

        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)

        self.assertFalse(truck.is_suitable(route))

    def test_is_suitable_insufficient_max_range(self):
        route = MagicMock()
        route.load = td.VALID_TRUCK_CAPACITY - 1000
        route.distance = td.VALID_TRUCK_MAX_RANGE + 1000  # Exceeds max range

        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)

        self.assertFalse(truck.is_suitable(route))

    def test_is_suitable_truck_is_busy(self):
        route = MagicMock()
        route.load = td.VALID_TRUCK_CAPACITY - 1000
        route.distance = td.VALID_TRUCK_MAX_RANGE - 1000

        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)
        truck.assigned_route_id = 1  # Truck is busy

        self.assertFalse(truck.is_suitable(route))

    def test_str_method(self):
        truck = Truck(name=td.VALID_TRUCK_NAME, capacity=td.VALID_TRUCK_CAPACITY, max_range=td.VALID_TRUCK_MAX_RANGE)
        expected_str = (
            f"TRUCK DETAILS:\n"
            f"ID: 1001\n"
            f"Name: {td.VALID_TRUCK_NAME}\n"
            f"Capacity: {td.VALID_TRUCK_CAPACITY}\n"
            f"Range: {td.VALID_TRUCK_MAX_RANGE}\n"
            f"Status: Free"
        )

        self.assertEqual(expected_str, str(truck))

        truck.assigned_route_id = 1
        expected_str_busy = (
            f"TRUCK DETAILS:\n"
            f"ID: 1001\n"
            f"Name: {td.VALID_TRUCK_NAME}\n"
            f"Capacity: {td.VALID_TRUCK_CAPACITY}\n"
            f"Range: {td.VALID_TRUCK_MAX_RANGE}\n"
            f"Status: Busy\nRoute ID: 1"
        )
        # expected should be in the first place
        self.assertEqual(expected_str_busy, str(truck))