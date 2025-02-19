import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import test_data as td
from skeleton.models.package import Package
from skeleton.models.route import Route
from skeleton.models.truck import Truck


class Route_Should(unittest.TestCase):

    def test_init(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        self.assertIsInstance(route.locations, tuple)
        self.assertIsInstance(route.departure_time, datetime)
        self.assertIsInstance(route.id, str)
        self.assertEqual(td.VALID_ID_LEN, len(route.id))
        self.assertEqual(None, route.assigned_truck)
        self.assertIsInstance(route.assigned_packages, tuple)
        self.assertEqual(0, route.load)
        self.assertIsInstance(route.stops, dict)

    @patch("builtins.print")
    def test_locations_invalidSeparator(self, mock_print):
        Route(td.INVALID_LOCATIONS_INPUT_SEPARATOR, td.VALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with(f"Locations should be separated by \"{Route.LOCATIONS_SEPARATOR}\"")

    @patch("builtins.print")
    def test_locations_invalidLocation(self, mock_print):
        Route(td.INVALID_LOCATIONS_INPUT_WRONG_LOCATION, td.VALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with("Invalid location: MIM.")

    @patch("builtins.print")
    def test_locations_invalidLocationsCount_noComma(self, mock_print):
        Route(td.INVALID_LOCATIONS_INPUT_TOO_FEW_WITHOUT_COMMA, td.VALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with(f"Locations should be separated by \"{Route.LOCATIONS_SEPARATOR}\"")

    @patch("builtins.print")
    def test_locations_invalidLocationsCount_withComma(self, mock_print):
        Route(td.INVALID_LOCATIONS_INPUT_TOO_FEW_WITH_COMMA, td.VALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with("Invalid location: .")

    @patch("builtins.print")
    def test_locations_raisesWhenTwoEqualLocations(self, mock_print):
        Route(td.INVALID_LOCATIONS_INPUT_TWO_ADJACENT_EQUAL, td.VALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with("Consecutive duplicate locations not allowed!")

    def test_locations_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_LOCATIONS_OUTPUT, route.locations)

    @patch("builtins.print")
    def test_departure_time_invalidString(self, mock_print):
        Route(td.VALID_LOCATIONS_INPUT, td.INVALID_DEPARTURE_TIME_INPUT)
        mock_print.assert_called_with(f"Departure time TestInvalidDepartureTime does not match "
                                                    f"the format dd/mm/YYYY-HH:MM")

    @patch("builtins.print")
    def test_departure_time_inThePast(self, mock_print):
        Route(td.VALID_LOCATIONS_INPUT, td.INVALID_DEPARTURE_TIME_IN_THE_PAST)
        mock_print.assert_called_with("Departure time must be in the future!")

    def test_departure_time_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_DEPARTURE_TIME_OUTPUT, route.departure_time)

    def test_id_length(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_ID_LEN, len(route.id))

    @patch("builtins.print")
    def test_assigned_truck_invalidTruck(self, mock_print):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.assigned_truck = td.INVALID_TRUCK
        mock_print.assert_called_with("Invalid truck!")

    @patch("builtins.print")
    def test_assigned_truck_notFree(self, mock_print):
        route_1 = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route_2 = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        truck.assign_to_route(route_1)
        route_2.assigned_truck = truck
        mock_print.assert_called_with("This truck is not free!")

    def test_assigned_truck_assignsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck = truck
        self.assertEqual(truck, route.assigned_truck)

    @patch("builtins.print")
    def test_free_capacity_raisesWhenNoAssignedTruck(self, mock_print):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        free_cap = route.free_capacity
        mock_print.assert_called_with("No truck assigned yet!")
        self.assertEqual(None, free_cap)

    def test_distance_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.VALID_DISTANCE, route.distance)

    def test_estimated_arrival_time_returnsCorrectly(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(td.EXPECTED_ESTIMATED_ARRIVAL_TIME, route.estimated_arrival_time)

    def test_status_returnsCorrectly_Created(self):
        current_time_plus_two_days = datetime.now() + timedelta(days=2)
        formatted_time = current_time_plus_two_days.strftime("%d/%m/%Y-%H:%M")
        route = Route(td.VALID_LOCATIONS_INPUT, formatted_time)
        self.assertEqual(Route.STATUS_CREATED, route.status)

    def my_now():
        if _my_custom_now is None:
            return datetime.datetime.now()
        else:
            return _my_custom_now
# @patch


    def test_status_returnsCorrectly_Finished(self):
        depart_time = datetime.now() + timedelta(days=2)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime("%d/%m/%Y-%H:%M"))

        with patch("datetime.datetime"):
            with patch("datetime.datetime.now", return_value=depart_time+timedelta(days=365*5)):
                self.assertEqual(Route.STATUS_FINISHED, route.status)

    def test_status_returnsCorrectly_InProgress(self):
        depart_time = datetime.now() + timedelta(days=2)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime("%d/%m/%Y-%H:%M"))

        with patch("datetime.datetime"):
            with patch("datetime.datetime.now", return_value=depart_time+timedelta(days=1)):
                self.assertEqual(Route.STATUS_IN_PROGRESS, route.status)

    def test_current_location_returnsCorrectly(self):
        depart_time = datetime.now() + timedelta(days=1)
        route = Route(td.VALID_LOCATIONS_INPUT, depart_time.strftime("%d/%m/%Y-%H:%M"))

        with patch("datetime.datetime"):
            with patch("datetime.datetime.now", return_value=route.departure_time+timedelta(days=1)):
                self.assertEqual(td.EXPECTED_CURRENT_LOCATION, route.current_location)

    @patch("builtins.print")
    def test_get_distance_invalidCity_1(self, mock_print):
        Route.get_distance(td.INVALID_CITY, td.VALID_CITY_2)
        mock_print.assert_called_with(f"Invalid city: {td.INVALID_CITY}")

    @patch("builtins.print")
    def test_get_distance_invalidCity_2(self, mock_print):
        Route.get_distance(td.VALID_CITY_1, td.INVALID_CITY)
        mock_print.assert_called_with(f"Invalid city: {td.INVALID_CITY}")

    @patch("builtins.print")
    def test_get_distance_equalCities(self, mock_print):
        Route.get_distance(td.VALID_CITY_1, td.VALID_CITY_1)
        mock_print.assert_called_with("Cities cannot be the same!")

    def test_get_distance_returnsCorrect(self):
        distance = Route.get_distance(td.VALID_CITY_1, td.VALID_CITY_2)
        self.assertEqual(td.EXPECTED_DISTANCE, distance)

    # To implement when Truck class is ready due to missing truck.id
    def test_str_returnsCorrectly_ifAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck("Scania", 42000, 8000)
        route.assign_truck(truck)
        EXPECTED_STR = f"Route Details:"
        f"\nID: {route.id}"
        f"\nHubs:\n{" -> ".join(f"{key}: {value}" for key, value in route.stops.items())}"
        f"\nDeparture Time: {route.departure_time.strftime("%d/%m/%Y %H:%M")}"
        f"\nNumber of Packages: {len(route.assigned_packages)}"
        f"\nCurrent Load: {route.load}"
        f"\nAssigned Truck ID: 1001"
        f"\nStatus: {route.status}"
        f"\nCurrent Location: {route.current_location}"
        f"\n============"


    def test_str_returnsCorrectly_ifNotAssignedTruck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        expected_str = (f"Route Details:"
                        f"\nID: {route.id}"
                        f"\nHubs:\nSYD: 2025-02-16 21:56:00 -> MEL: 2025-02-17 08:01:00 -> BRI: 2025-02-18 04:18:00"
                        f"\nDeparture Time: 16/02/2025 11:30"
                        f"\nNumber of Packages: 0"
                        f"\nCurrent Load: 0"
                        f"\nStatus: Created"
                        f"\nCurrent Location: None"
                        f"\n============")

        self.assertEqual(expected_str, str(route))

    def test_calculating_estimated_arrival_times(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)

        self.assertEqual(td.EXPECTED_STOPS, route.stops)

    # To be further implemented when Truck class is ready
    def test_assign_truck(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck("Scania", 42000, 8000)
        route.assign_truck(truck)
        self.assertEqual(truck, route.assigned_truck)

    @patch("builtins.print")
    def test_remove_truck_whenNoTruck(self, mock_print):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.remove_truck()
        mock_print.assert_called_with("No truck assigned to this route!")

    # To be further implemented when Truck class is ready
    def test_remove_truck_whenAssigned(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck("Scania", 42000, 8000)
        route.assign_truck(truck)
        route.remove_truck()
        self.assertIsNone(route.assigned_truck)

    @patch("builtins.print")
    def test_assign_package_invalidPackage(self, mock_print):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.assign_package(td.INVALID_PACKAGE)
        mock_print.assert_called_with("Invalid package")

    # To be further implemented when Truck class is ready
    @patch("builtins.print")
    def test_assign_package_noCapacity(self, mock_print):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck("Scania", 42000, 8000)
        route.assign_truck(truck)
        package = Package("SYD", "MEL", 80000, "abc@gmail.com")
        route.assign_package(package)
        mock_print.assert_called_with("No more capacity")

    # To be further implemented when Truck class is ready
    def test_assign_package(self):
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck("Scania", 42000, 8000)
        route.assigned_truck = truck
        package = Package("SYD", "MEL", 80, "abc@gmail.com")
        route.assign_package(package)

        self.assertIn(package, route.assigned_packages)
        self.assertEqual(route, package.route)
        self.assertEqual(1, len(route.assigned_packages))

