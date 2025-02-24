import unittest
from unittest.mock import Mock
import test_data as td
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
        with self.assertRaises(ApplicationError):
            SearchRouteCommand(["a"] * 0, Mock())

    def test_initializer_raisesError_tooManyParamsCount(self):
        with self.assertRaises(ApplicationError):
            SearchRouteCommand(["a"] * 3, Mock())

    def test_initializer_passes_validParamsCount(self):
        SearchRouteCommand(["a"] * 1, Mock())

    def test_execute_startLocationNotIn(self):
        app_data = ApplicationData()
        package = Package("PER", td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual("Suitable Routes:\n", output)

    def test_execute_endLocationNotIn(self):
        app_data = ApplicationData()
        package = Package( td.VALID_START_LOCATION, "PER", td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual("Suitable Routes:\n", output)

    def test_execute_endLocationBeforeStart(self):
        app_data = ApplicationData()
        package = Package(td.VALID_END_LOCATION, td.VALID_START_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual("Suitable Routes:\n", output)

    def test_execute_insufficientCapacity(self):
        app_data = ApplicationData()
        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, 43000, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual("Suitable Routes:\n", output)

    def test_execute_noRoutes(self):
        app_data = ApplicationData()
        package = Package(td.VALID_START_LOCATION, "PER", td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        app_data._packages.append(package)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual("Suitable Routes:\n", output)

    def test_execute_searchesRoute_validParams_whenOneRoute(self):
        app_data = ApplicationData()
        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        truck = Truck(td.VALID_TRUCK_NAME, td.VALID_TRUCK_CAPACITY, td.VALID_TRUCK_MAX_RANGE)
        route.assigned_truck_id = truck.id
        app_data._packages.append(package)
        app_data._routes.append(route)
        app_data._trucks.append(truck)
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual(f"Suitable Routes:"
                         f"\nRoute Details:"
                         f"\nID: {route.id}"
                         f"\nHubs:"
                         f"\nSYD: 2055-02-16 11:30:00 -> MEL: 2055-02-16 21:34:49.655172 -> BRI: 2055-02-17 17:52:04.137931"
                         f"\nDeparture Time: 2055-02-16 11:30"
                         "\n============",
                         output)

    def test_execute_searchesRoute_validParams_whenManyRoutes(self):
        app_data = ApplicationData()
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
        cmd = SearchRouteCommand([package.id], app_data)
        output = cmd.execute()

        self.assertEqual(f"Suitable Routes:"
                         f"\nRoute Details:"
                         f"\nID: {route_1.id}"
                         f"\nHubs:"
                         f"\nSYD: 2055-02-16 11:30:00 -> MEL: 2055-02-16 21:34:49.655172 -> BRI: 2055-02-17 17:52:04.137931"
                         f"\nDeparture Time: 2055-02-16 11:30"
                         "\n============"
                         f"\nRoute Details:"
                         f"\nID: {route_2.id}"
                         f"\nHubs:"
                         f"\nSYD: 2055-02-16 11:30:00 -> MEL: 2055-02-16 21:34:49.655172 -> BRI: 2055-02-17 17:52:04.137931"
                         f"\nDeparture Time: 2055-02-16 11:30"
                         "\n============",
                         output)
