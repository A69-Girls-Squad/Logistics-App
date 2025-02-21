import unittest
from unittest.mock import Mock

from commands.create_route import CreateRouteCommand
from commands.search_route import SearchRouteCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError



def _create_fake_params(
        *,
        locations="SYD,MEL,BRI",
        departure_time="16/02/2055-11:30"):
    return [locations, departure_time]


class SearchRouteCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        with self.assertRaises(ApplicationError):
            SearchRouteCommand(["a"] * 0, Mock())

    def test_initializer_raisesError_tooManyParamsCount(self):
        with self.assertRaises(ApplicationError):
            SearchRouteCommand(["a"] * 3, Mock())

    def test_initializer_passes_validParamsCount(self):
        SearchRouteCommand(["a"] * 1, Mock())

    def test_execute_searchesRoute_validParams(self):
        fake_params = _create_fake_params()
        app_data = ApplicationData()
        cmd = CreateRouteCommand(fake_params, app_data)

        output = cmd.execute()

        self.assertEqual(
            f"Route with id 1 was created!"
            f"\nLocations: {fake_params[0]}"
            f"\nDeparture Time: {fake_params[1]}", output)

    def test_execute_raisesError_invalidLocations(self):
        from errors.application_error import ApplicationError
        app_data = ApplicationData()
        cmd = CreateRouteCommand(_create_fake_params(locations="SYD"),app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_execute_raisesError_invalidDeparture_time(self):
        app_data = ApplicationData()
        cmd = CreateRouteCommand(_create_fake_params(departure_time="TestInvalidDepartureTime"), app_data)

        with self.assertRaises(ValueError):
            cmd.execute()