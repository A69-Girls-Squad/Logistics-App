import unittest
from unittest.mock import Mock
import test_data as td
from commands.base_command import BaseCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from models.package import Package
from models.route import Route
from models.truck import Truck
from commands.search_route import SearchRouteCommand


def _create_fake_params_package(
    *,
    start_location = "SYD",
    end_location = "MEL",
    weight = 50,
    customer_email = "customer@gmail.com"):
    return [start_location, end_location, weight, customer_email]

def _create_fake_params_route(
    *,
    locations  = "SYD,MEL,BRI",
    departure_time="16/02/2055 11:30"):
    return [locations, departure_time]


class SearchRouteCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        cmd = SearchRouteCommand(["a"] * 0, Mock())
        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_initializer_raisesError_tooManyParamsCount(self):
        cmd = SearchRouteCommand(["a"] * 3, Mock())
        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_initializer_passes_validParamsCount(self):
        SearchRouteCommand(["a"] * 1, Mock())

    def test_execute_startLocationNotIn(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package("PER", td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()

        expected_message = f"SUITABLE ROUTES:\n{BaseCommand.ROW_SEP}\n{BaseCommand.TABLE_SEP}\n"
        self.assertEqual(expected_message, output)

    def test_execute_endLocationNotIn(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package( td.VALID_START_LOCATION, "PER", td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = f"SUITABLE ROUTES:\n{BaseCommand.ROW_SEP}\n{BaseCommand.TABLE_SEP}\n"

        self.assertEqual(expected_message, output)

    def test_execute_endLocationBeforeStart(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package(td.VALID_END_LOCATION, td.VALID_START_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = f"SUITABLE ROUTES:\n{BaseCommand.ROW_SEP}\n{BaseCommand.TABLE_SEP}\n"

        self.assertEqual(expected_message, output)

    def test_execute_insufficientCapacity(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, 43000, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = f"SUITABLE ROUTES:\n{BaseCommand.ROW_SEP}\n{BaseCommand.TABLE_SEP}\n"

        self.assertEqual(expected_message, output)

    def test_execute_noRoutes(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package(td.VALID_START_LOCATION, "PER", td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        app_data._packages.append(package)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = f"SUITABLE ROUTES:\n{BaseCommand.ROW_SEP}\n{BaseCommand.TABLE_SEP}\n"

        self.assertEqual(expected_message, output)

    def test_execute_searchesRoute_validParams_whenOneRoute(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = (f"SUITABLE ROUTES:"
                            f"\n{BaseCommand.ROW_SEP}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nROUTE ID:       | {route.id}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nHubs:           | SYD: 2055-02-16 11:30"
                            f"\n                | MEL: 2055-02-16 21:34"
                            f"\n                | BRI: 2055-02-17 17:52"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nDeparture time: | 2055-02-16 11:30"
                            f"\n{BaseCommand.ROW_SEP}")

        self.assertEqual(expected_message, output)

    def test_execute_searchesRoute_validParams_whenManyRoutes(self):
        app_data = ApplicationData()
        app_data.logged_in_employee = Mock()

        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route_1 = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route_2 = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck_1 = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        truck_2 = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route_1.assigned_truck_id = truck_1.id
        route_2.assigned_truck_id = truck_2.id
        app_data._packages.append(package)
        app_data._routes.append(route_1)
        app_data._routes.append(route_2)
        app_data._trucks.append(truck_1)
        app_data._trucks.append(truck_2)
        cmd = SearchRouteCommand([str(package.id)], app_data)
        output = cmd.execute()
        expected_message = (f"SUITABLE ROUTES:"
                            f"\n{BaseCommand.ROW_SEP}"
                            f"\n{BaseCommand.TABLE_SEP}\n"
                            f"ROUTE ID:       | {route_1.id}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nHubs:           | SYD: 2055-02-16 11:30"
                            f"\n                | MEL: 2055-02-16 21:34"
                            f"\n                | BRI: 2055-02-17 17:52"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nDeparture time: | "
                            f"2055-02-16 11:30"
                            f"\n{BaseCommand.ROW_SEP}"
                            f"\nROUTE ID:       | {route_2.id}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nHubs:           | SYD: 2055-02-16 11:30"
                            f"\n                | MEL: 2055-02-16 21:34"
                            f"\n                | BRI: 2055-02-17 17:52"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nDeparture time: | "
                            f"2055-02-16 11:30"
                            f"\n{BaseCommand.ROW_SEP}"
                            )

        self.assertEqual(expected_message, output)
