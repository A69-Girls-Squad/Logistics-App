import unittest
from unittest.mock import Mock

from commands.create_route import CreateRouteCommand
from errors.application_error import ApplicationError


def _create_fake_params(
        *,
        locations="SYD,MIM,BRI",
        departure_time="16/02/2025-11:30"):
    return [locations, departure_time]


def _create_mock():
    fake_data = Mock()

    def create_route(locations, departure_time):
        route = Mock()
        route.locations = locations
        route.departure_time = departure_time
        fake_data.routes.append(route)

        return route

    fake_data.routes = []
    fake_data.create_route = create_route

    return fake_data


class CreateRouteCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        with self.assertRaises(ApplicationError):
            CreateRouteCommand(["a" * 1], _create_mock())

    def test_initializer_raisesError_tooManyParamsCount(self):
        with self.assertRaises(ApplicationError):
            CreateRouteCommand(["a" * 3], _create_mock())

    def test_initializer_passes_validParamsCount(self):
        with self.assertRaises(ApplicationError):
            CreateRouteCommand(["a" * 2], _create_mock())

    def test_execute_createsRoute_validParams(self):
        fake_params = _create_fake_params()
        cmd = CreateRouteCommand(fake_params, _create_mock())

        output = cmd.execute()

        self.assertEqual(
            f"Route with locations {fake_params[0]} was created!", output)

    def test_execute_raisesError_invalidLocations(self):
        cmd = CreateRouteCommand(_create_fake_params(locations="SYD"),_create_mock())

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_execute_raisesError_invalidDeparture_time(self):
        cmd = CreateRouteCommand(
            _create_fake_params(departure_time="TestInvalidDepartureTime"),
            _create_mock())

        with self.assertRaises(ApplicationError):
            cmd.execute()