import unittest
from unittest.mock import MagicMock
from commands.assign_truck_to_route import AssignTruckToRouteCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError

class TestAssignTruckToRouteCommand(unittest.TestCase):

    def test_execute_successful(self):
        params = ["1001","11"]
        app_data_mock = MagicMock(ApplicationData)

        app_data_mock.assign_truck_to_route = MagicMock()

        cmd = AssignTruckToRouteCommand(params, app_data_mock)
        output = cmd.execute()

        self.assertEqual(output, "Truck with id 1001 assigned to route 11")

    def test_invalid_params_count(self):
        params = ["1001"]
        app_data_mock = MagicMock(ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_invalid_truck_id(self):
        params = ["text", "11"]
        app_data_mock = MagicMock(ApplicationData)

        cmd = AssignTruckToRouteCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()