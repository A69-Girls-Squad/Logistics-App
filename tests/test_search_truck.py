import unittest
from unittest.mock import MagicMock
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from commands.search_truck import SearchTruckCommand


class TestSearchTruckCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["11"]
        app_data_mock = MagicMock(spec=ApplicationData)

        route_mock = MagicMock()
        app_data_mock.find_route_by_id.return_value = route_mock

        truck1_mock = MagicMock()
        truck2_mock = MagicMock()

        truck1_mock.id = 1001
        truck1_mock.name = "Truck A"
        truck1_mock.capacity = 5000
        truck1_mock.max_range = 300
        truck1_mock.is_suitable.return_value = True

        truck2_mock.id = 1002
        truck2_mock.name = "Truck B"
        truck2_mock.capacity = 4000
        truck2_mock.max_range = 250
        truck2_mock.is_suitable.return_value = False

        app_data_mock.trucks = [truck1_mock, truck2_mock]

        cmd = SearchTruckCommand(params, app_data_mock)

        output = cmd.execute()

        expected_output = (
                f"TRUCK ID: 1001 Truck A | Capacity: 5000 | Max Range: 300\n" + "-" * 60
        )

        self.assertIn(expected_output, output)
        self.assertNotIn("TRUCK ID: 1002", output)

    def test_invalid_params_count(self):
        params = []
        app_data_mock = MagicMock(spec=ApplicationData)

        with self.assertRaises(ApplicationError):
            SearchTruckCommand(params, app_data_mock)

    def test_route_not_found(self):
        params = ["11"]
        app_data_mock = MagicMock(spec=ApplicationData)

        app_data_mock.find_route_by_id.return_value = None

        cmd = SearchTruckCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_no_suitable_trucks(self):
        params = ["11"]
        app_data_mock = MagicMock(spec=ApplicationData)

        route_mock = MagicMock()
        app_data_mock.find_route_by_id.return_value = route_mock

        truck_mock = MagicMock()
        app_data_mock.trucks = [truck_mock]
        truck_mock.is_suitable.return_value = False

        cmd = SearchTruckCommand(params, app_data_mock)

        expected_output = "No available truck found" + cmd.ROW_SEP
        output = cmd.execute()

        self.assertEqual(output, expected_output)