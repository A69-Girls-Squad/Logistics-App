import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import test_data as td
from errors.application_error import ApplicationError
from models.constants.distances import Distance
from models.route import Route
from models.truck import Truck
from interface_menu import TABLE_SEP, ROW_SEP


class Route_Should(unittest.TestCase):

    def test_init(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        self.assertIsInstance(route.locations, tuple)
        self.assertIsInstance(route.departure_time, datetime)
        self.assertIsInstance(route.id, int)
        self.assertEqual(None, route.assigned_truck_id)
        self.assertIsInstance(route.assigned_packages_ids, tuple)
        self.assertEqual(0, route.load)
        self.assertIsInstance(route.stops, dict)

    def test_locations_invalidSeparator(self):
        with self.assertRaises(ApplicationError):
            Route(td.INVALID_LOCATIONS_INPUT_SEPARATOR, td.VALID_DEPARTURE_TIME_INPUT)

    def test_locations_invalidLocation(self):
        with self.assertRaises(ApplicationError):
            Route(td.INVALID_LOCATIONS_INPUT_WRONG_LOCATION, td.VALID_DEPARTURE_TIME_INPUT)

    def test_locations_invalidLocationsCount_noComma(self):
        with self.assertRaises(ApplicationError):
            Route(td.INVALID_LOCATIONS_INPUT_TOO_FEW_WITHOUT_COMMA, td.VALID_DEPARTURE_TIME_INPUT)

    def test_locations_invalidLocationsCount_withComma(self):
        with self.assertRaises(ApplicationError):
            Route(td.INVALID_LOCATIONS_INPUT_TOO_FEW_WITH_COMMA, td.VALID_DEPARTURE_TIME_INPUT)

    def test_locations_raisesWhenTwoEqualLocations(self):
        with self.assertRaises(ApplicationError):
            Route(td.INVALID_LOCATIONS_INPUT_TWO_ADJACENT_EQUAL, td.VALID_DEPARTURE_TIME_INPUT)

    def test_locations_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_LOCATIONS_OUTPUT, route.locations)

    def test_departure_time_invalidString(self):
        with self.assertRaises(ApplicationError):
            Route(td.VALID_LOCATIONS_INPUT, td.INVALID_DEPARTURE_TIME_INPUT)

    def test_departure_time_inThePast(self):
        with self.assertRaises(ApplicationError):
            Route(td.VALID_LOCATIONS_INPUT, td.INVALID_DEPARTURE_TIME_IN_THE_PAST)

    def test_departure_time_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_DEPARTURE_TIME_OUTPUT, route.departure_time)

    def test_assigned_truck_assignsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck = truck
        self.assertEqual(truck, route.assigned_truck)

    def test_distance_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_DISTANCE, route.distance)

    def test_estimated_arrival_time_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.EXPECTED_ESTIMATED_ARRIVAL_TIME, route.estimated_arrival_time)

    def test_status_returnsCorrectly_Created(self):
        current_time_plus_two_days = datetime.now() + timedelta(days=2)
        formatted_time = current_time_plus_two_days.isoformat()
        route = Route(td.VALID_LOCATIONS_INPUT, formatted_time)
        self.assertEqual(Route.STATUS_CREATED, route.status)

    def test_get_distance_returnsCorrect(self):
        distance = Distance.get_distance(td.VALID_CITY_1, td.VALID_CITY_2)
        self.assertEqual(td.EXPECTED_DISTANCE, distance)

    def test_str_returnsCorrectly_ifAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assign_truck(truck.id)
        expected_str = (f"ROUTE DETAILS:\n{TABLE_SEP}"
                        f"\nID:             | {route.id}\n{TABLE_SEP}"
                        f"\nHubs:           | {"\n                | ".join(f"{key}: {value.isoformat(sep=" ", timespec="minutes")}"
                                                                           for key, value in route.stops.items())}\n{TABLE_SEP}"
                        f"\nDeparture time: | 2055-02-16 11:30\n{TABLE_SEP}"
                        f"\nPackages count: | {len(route.assigned_packages_ids)}\n{TABLE_SEP}"
                        f"\nCurrent load:   | {route.load}\n{TABLE_SEP}"
                        f"\nTruck Info:     | Assigned Truck ID: {route.assigned_truck_id}\n{TABLE_SEP}"
                        f"\nStatus:         | {route.status}\n{ROW_SEP}")

        self.assertEqual(expected_str, str(route))

    def test_str_returnsCorrectly_ifNotAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        expected_str = (f"ROUTE DETAILS:\n{TABLE_SEP}"
                        f"\nID:             | {route.id}\n{TABLE_SEP}"
                        f"\nHubs:           | {"\n                | ".join(f"{key}: {value.isoformat(sep=" ", timespec="minutes")}"
                                                                           for key, value in route.stops.items())}\n{TABLE_SEP}"
                        f"\nDeparture time: | 2055-02-16 11:30\n{TABLE_SEP}"
                        f"\nPackages count: | {len(route.assigned_packages_ids)}\n{TABLE_SEP}"
                        f"\nCurrent load:   | {route.load}\n{TABLE_SEP}"
                        f"\nTruck Info:     | No truck assigned.\n{TABLE_SEP}"
                        f"\nStatus:         | {route.status}\n{ROW_SEP}")

        self.assertEqual(expected_str, str(route))

    def test_calculating_estimated_arrival_times(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        self.assertEqual(td.EXPECTED_STOPS, route.stops)

    def test_assign_truck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assign_truck(truck)
        self.assertEqual(truck, route.assigned_truck_id)
