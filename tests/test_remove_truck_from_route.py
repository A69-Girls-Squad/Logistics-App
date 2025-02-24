import unittest
from unittest.mock import MagicMock
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from commands.remove_truck_from_route import RemoveTruckFromRouteCommand


class TestRemoveTruckFromRouteCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(ApplicationData)

        truck_mock = MagicMock()
        route_mock = MagicMock()

        app_data_mock.find_truck_by_id.return_value = truck_mock
        app_data_mock.find_route_by_id.return_value = route_mock

        truck_mock.assigned_route = route_mock
        truck_mock.remove_from_route = MagicMock()

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        output = cmd.execute()

        expected_output = (
            "Truck with ID 1001 has been removed from Route 11, truck status changed to free."
            + cmd.ROW_SEP_LONG
        )
        self.assertEqual(output, expected_output)

    def test_invalid_params_count(self):
        params = ["1001"]
        app_data_mock = MagicMock(ApplicationData)

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_truck_not_found(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(ApplicationData)

        app_data_mock.find_truck_by_id.return_value = None

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_route_not_found(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(ApplicationData)

        truck_mock = MagicMock()
        app_data_mock.find_truck_by_id.return_value = truck_mock

        app_data_mock.find_route_by_id.return_value = None

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_truck_not_assigned_to_route(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(ApplicationData)

        truck_mock = MagicMock()
        app_data_mock.find_truck_by_id.return_value = truck_mock

        route_mock = MagicMock()
        app_data_mock.find_route_by_id.return_value = route_mock

        truck_mock.assigned_route = MagicMock()

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()