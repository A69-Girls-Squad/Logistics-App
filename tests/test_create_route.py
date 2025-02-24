import unittest
from unittest.mock import Mock

from commands.base_command import BaseCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from commands.create_route import CreateRouteCommand


def _create_fake_params(
        *,
        locations="SYD,MEL,BRI",
        departure_time="2055-02-16 11:30"):
    return [locations, departure_time]


class CreateRouteCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        with self.assertRaises(ApplicationError):
            CreateRouteCommand(["a"] * 1, Mock())

    def test_initializer_raisesError_tooManyParamsCount(self):
        with self.assertRaises(ApplicationError):
            CreateRouteCommand(["a"] * 3, Mock())

    def test_initializer_passes_validParamsCount(self):
        CreateRouteCommand(["a"] * 2, Mock())

    def test_execute_createsRoute_validParams(self):
        fake_params = _create_fake_params()
        app_data = ApplicationData()
        cmd = CreateRouteCommand(fake_params, app_data)

        output = cmd.execute()
        expected_message = (f"Route with ID 1 was created!"
                f"\n{BaseCommand.TABLE_SEP}"
                f"\nLocations:      | {fake_params[0]}"
                f"\n{BaseCommand.TABLE_SEP}"
                f"\nDeparture Time: | {fake_params[1]}"
                f"\n{BaseCommand.TABLE_SEP}") + BaseCommand.ROW_SEP*2
        self.assertEqual(expected_message, output)

    def test_execute_raisesError_invalidLocations(self):
        app_data = ApplicationData()
        cmd = CreateRouteCommand(_create_fake_params(locations="SYD"),app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_execute_raisesError_invalidDeparture_time(self):
        app_data = ApplicationData()
        cmd = CreateRouteCommand(_create_fake_params(departure_time="TestInvalidDepartureTime"), app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()