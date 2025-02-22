import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import test_data as td
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from main import app_data
from models.constants.distances import Distance
from models.route import Route
from models.truck import Truck


def my_now(_my_custom_now):
    if _my_custom_now is None:
        return datetime.now()
    else:
        return _my_custom_now

# def get_current_time():
#     return datetime.now()
#
# @patch("datetime.datetime")
# def custom_now(mock_datetime):
#     fixed_time = datetime(2555, 1, 1, 12, 0)
#     mock_datetime.now.return_value = fixed_time
#     return get_current_time()


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
        with self.assertRaises(ValueError):
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

    def test_free_capacity_raisesWhenNoAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        with self.assertRaises(ApplicationError):
            free_cap = route.free_capacity
            self.assertEqual(None, free_cap)

    def test_distance_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_DISTANCE, route.distance)

    def test_estimated_arrival_time_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.EXPECTED_ESTIMATED_ARRIVAL_TIME, route.estimated_arrival_time)

    def test_status_returnsCorrectly_Created(self):
        current_time_plus_two_days = datetime.now() + timedelta(days=2)
        formatted_time = current_time_plus_two_days.strftime(td.VALID_DATETIME_FORMAT)
        route = Route(td.VALID_LOCATIONS_INPUT, formatted_time)
        self.assertEqual(Route.STATUS_CREATED, route.status)

    def test_status_returnsCorrectly_Finished(self):
        depart_time = datetime.now() + timedelta(days=2)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime(td.VALID_DATETIME_FORMAT))

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = depart_time + timedelta(days=365 * 5)
            self.assertEqual(Route.STATUS_FINISHED, route.status)

    def test_status_returnsCorrectly_InProgress(self):
        depart_time = datetime.now() + timedelta(days=2)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime(td.VALID_DATETIME_FORMAT))

        with patch("datetime.datetime"):
            with patch("datetime.datetime.now", return_value=depart_time+timedelta(days=1)):
                self.assertEqual(Route.STATUS_IN_PROGRESS, route.status)

    def test_current_location_returnsCorrectly(self):
        depart_time = datetime.now() + timedelta(days=1)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime(td.VALID_DATETIME_FORMAT))

        with patch("datetime.datetime"):
            with patch("datetime.datetime.now", return_value=route.departure_time+timedelta(days=1)):
                self.assertEqual(td.EXPECTED_CURRENT_LOCATION, route.current_location)

    def test_get_distance_invalidCity_1(self):
        with self.assertRaises(ApplicationError):
            Distance.get_distance(td.INVALID_CITY, td.VALID_CITY_2)

    def test_get_distance_invalidCity_2(self):
        with self.assertRaises(ApplicationError):
            Distance.get_distance(td.VALID_CITY_1, td.INVALID_CITY)

    def test_get_distance_equalCities(self):
        with self.assertRaises(ApplicationError):
            Distance.get_distance(td.VALID_CITY_1, td.VALID_CITY_1)

    def test_get_distance_returnsCorrect(self):
        distance = Distance.get_distance(td.VALID_CITY_1, td.VALID_CITY_2)
        self.assertEqual(td.EXPECTED_DISTANCE, distance)

    def test_str_returnsCorrectly_ifAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_CAPACITY, td.VALID_MAX_RANGE)
        route.assign_truck(truck)
        expected_str = (f"Route Details:"
                        f"\nID: {route.id}"
                        f"\nHubs:\n{" -> ".join(f"{key}: {value}" for key, value in route.stops.items())}"
                        f"\nDeparture Time: 2055-02-16 11:30"
                        f"\nNumber of Packages: {len(route.assigned_packages_ids)}"
                        f"\nCurrent Load: {route.load}"
                        f"\nStatus: {route.status}"
                        f"\nCurrent Location: {route.current_location}"
                        f"\n============")

        self.assertEqual(expected_str, str(route))

    def test_str_returnsCorrectly_ifNotAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        expected_str = (f"Route Details:"
                        f"\nID: {route.id}"
                        f"\nHubs:"
                        f"\nSYD: 2055-02-16 21:56:00 -> MEL: 2055-02-17 08:01:00 -> BRI: 2055-02-18 04:18:00"
                        f"\nDeparture Time: 2055-02-16 11:30"
                        f"\nNumber of Packages: 0"
                        f"\nCurrent Load: 0"
                        f"\nStatus: Created"
                        f"\nCurrent Location: None"
                        f"\n============")

        self.assertEqual(expected_str, str(route))

    def test_calculating_estimated_arrival_times(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        self.assertEqual(td.EXPECTED_STOPS, route.stops)

    def test_assign_truck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_CAPACITY, td.VALID_MAX_RANGE)
        route.assign_truck(truck)
        self.assertEqual(truck, route.assigned_truck_id)

    def test_remove_truck_whenNoTruck(self):
        with self.assertRaises(ApplicationError):
            route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
            route.remove_truck()

    def test_remove_truck_whenAssigned(self):
        app_data = ApplicationData()
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_CAPACITY, td.VALID_MAX_RANGE)
        route.assign_truck(truck)
        route.remove_truck()
        self.assertIsNone(route.assigned_truck_id)