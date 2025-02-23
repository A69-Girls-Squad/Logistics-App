import unittest
from unittest.mock import MagicMock
from skeleton.commands.search_truck import SearchTruckCommand
from skeleton.core.application_data import ApplicationData
from skeleton.errors.application_error import ApplicationError
class TestSearchTruckCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["11"] 
        app_data_mock = MagicMock(ApplicationData)
        
        route_mock = MagicMock()
        app_data_mock.find_route_by_id.return_value = route_mock

        truck1_mock = MagicMock()
        truck2_mock = MagicMock()

        app_data_mock.trucks = [truck1_mock, truck2_mock]

        truck1_mock.is_suitable.return_value = True
        truck2_mock.is_suitable.return_value = False

        cmd = SearchTruckCommand(params, app_data_mock)

        output = cmd.execute()

        self.assertIn(str(truck1_mock), output)
        self.assertNotIn(str(truck2_mock), output)

    def test_invalid_params_count(self):
        params = []
        app_data_mock = MagicMock(ApplicationData)

        cmd = SearchTruckCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_route_not_found(self):
        params = ["11"]
        app_data_mock = MagicMock(ApplicationData)

        app_data_mock.find_route_by_id.return_value = None

        cmd = SearchTruckCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_no_suitable_trucks(self):
        params = ["11"]
        app_data_mock = MagicMock(ApplicationData)

        route_mock = MagicMock()
        app_data_mock.find_route_by_id.return_value = route_mock

        truck_mock = MagicMock()
        app_data_mock.trucks = [truck_mock]
        truck_mock.is_suitable.return_value = False

        cmd = SearchTruckCommand(params, app_data_mock)

        output = cmd.execute()
        self.assertEqual(output, "No available truck found")