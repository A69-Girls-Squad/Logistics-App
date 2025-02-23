import unittest
from unittest.mock import MagicMock, patch
from commands.assign_truck_to_route import AssignTruckToRouteCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class TestAssignTruckToRouteCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["1001", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)
        app_data_mock.logged_in_employee = "John Doe"
        app_data_mock.assign_truck_to_route = MagicMock()

        cmd = AssignTruckToRouteCommand(params, app_data_mock)
        output = cmd.execute()

        self.assertEqual(output, "Truck with id 1001 assigned to route 11")
        app_data_mock.assign_truck_to_route.assert_called_once_with(1001, 11)

    def test_invalid_params_count(self):
        params = ["1001"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    @patch("commands.validation_helpers.try_parse_int", side_effect=ValueError)
    def test_invalid_truck_id(self, mock_try_parse_int):
        params = ["text", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    @patch("commands.validation_helpers.try_parse_int", side_effect=[1001, ValueError])
    def test_invalid_route_id(self, mock_try_parse_int):
        params = ["1001", "invalid"]
        app_data_mock = MagicMock(spec=ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    @patch("commands.assign_truck_to_route.logging.getLogger")
    def test_logger_called(self, mock_get_logger):
        params = ["1001", "11"]
        app_data_mock = MagicMock(spec=ApplicationData)
        app_data_mock.logged_in_employee = "John Doe"
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        cmd = AssignTruckToRouteCommand(params, app_data_mock)
        cmd.execute()

        expected_log_message = "Truck with id 1001 assigned to route 11 | Executed by: John Doe"
        mock_logger.info.assert_called_with(expected_log_message)
