import unittest
from unittest.mock import MagicMock
from commands.assign_truck_to_route import AssignTruckToRouteCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class TestAssignTruckToRouteCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)
        app_data_mock.logged_in_employee = "Test User"
        app_data_mock.assign_truck_to_route = MagicMock()

        cmd = AssignTruckToRouteCommand(params, app_data_mock)
        output = cmd.execute()

        expected_output = "Truck with id 1001 assigned to route 11" + cmd.ROW_SEP_LONG
        self.assertEqual(output, expected_output)
        app_data_mock.assign_truck_to_route.assert_called_once_with(1001, 11)

    def test_invalid_params_count(self):
        params = ["1001"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_invalid_truck_id(self):
        params = ["text", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_invalid_route_id(self):
        params = ["1001", "invalid"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_logger_called(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)
        app_data_mock.logged_in_employee = "Test User"

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertLogs(cmd.logger, level="INFO") as log:
            cmd.execute()

        expected_log_message = "Truck with id 1001 assigned to route 11 | Executed by: Test User"
        self.assertIn(expected_log_message, log.output[0])