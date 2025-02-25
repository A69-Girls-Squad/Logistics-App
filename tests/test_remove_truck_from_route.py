import unittest
from unittest.mock import MagicMock
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from commands.remove_truck_from_route import RemoveTruckFromRouteCommand


class TestRemoveTruckFromRouteCommand(unittest.TestCase):

    def test_execute_successful(self):
        # Fix: Only pass one parameter (truck ID)
        params = ["1001"]
        app_data_mock = MagicMock(spec=ApplicationData)

        # Mock a truck with an assigned route
        truck_mock = MagicMock()
        truck_mock.id = 1001
        truck_mock.assigned_route_id = 11  # Corrected assignment

        app_data_mock.find_truck_by_id.return_value = truck_mock
        app_data_mock.unassign_truck_from_route = MagicMock()
        app_data_mock.logged_in_employee.username = "TestUser"

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)
        output = cmd.execute()

        expected_output = (
            "Truck with ID 1001 has been removed from Route ID 11, "
            "Truck status changed to \"free\"."
        )
        self.assertEqual(output, expected_output)
        app_data_mock.unassign_truck_from_route.assert_called_once_with(1001)

    def test_invalid_params_count(self):
        # Fix: Pass an empty list to trigger param count error
        params = []
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_truck_not_found(self):
        params = ["1001"]
        app_data_mock = MagicMock(spec=ApplicationData)
        app_data_mock.find_truck_by_id.return_value = None  # Ensure it returns None

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_truck_not_assigned_to_route(self):
        params = ["1001"]
        app_data_mock = MagicMock(spec=ApplicationData)

        truck_mock = MagicMock()
        truck_mock.id = 1001
        truck_mock.assigned_route_id = None

        app_data_mock.find_truck_by_id.return_value = truck_mock

        cmd = RemoveTruckFromRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()