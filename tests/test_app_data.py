import unittest
from unittest.mock import patch

import test_data as td
from core.application_data import ApplicationData
from models.employee import Employee
from skeleton.models.package import Package
from skeleton.models.route import Route


class ApplicationData_Should(unittest.TestCase):

    def test_init(self):
        app_data = ApplicationData()

        self.assertIsInstance(app_data.trucks, tuple)
        self.assertIsInstance(app_data.routes, tuple)
        self.assertIsInstance(app_data.packages, tuple)
        self.assertIsInstance(app_data.employees, tuple)
        self.assertIsNone(app_data.logged_in_employee)

    @patch("builtins.print")
    def test_logged_in_employee_raisesWhenInvalidEmployee(self, mock_print):
        app_data = ApplicationData()
        app_data.logged_in_employee = td.INVALID_EMPLOYEE
        self.assertFalse(app_data.has_logged_in_employee)
        mock_print.assert_called_with("Invalid employee")

    def test_logged_in_employee_returnsCorrectly(self):
        app_data = ApplicationData()
        employee = Employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                            td.VALID_EMPLOYEE_ROLE)
        app_data.login(employee)
        self.assertEqual(employee, app_data.logged_in_employee)

    def test_has_logged_in_employee_whenNone(self):
        app_data = ApplicationData()
        self.assertFalse(app_data.has_logged_in_employee)

    def test_has_logged_in_employee_whenHas(self):
        app_data = ApplicationData()
        employee = Employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                            td.VALID_EMPLOYEE_ROLE)
        app_data.logged_in_employee = employee
        self.assertTrue(app_data.has_logged_in_employee)

    def test_not_assigned_packages_noPackages(self):
        app_data = ApplicationData()
        self.assertEqual([], app_data.not_assigned_packages)

    def test_not_assigned_packages_noNotAssigned(self):
        app_data = ApplicationData()
        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.assign_package(package)
        self.assertEqual([], app_data.not_assigned_packages)

    # Tobe further implemented when Package class is ready because of incorrect Package.is_assigned attribute
    def test_not_assigned_packages_returnsCorrectly(self):
        app_data = ApplicationData()
        package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT, td.VALID_CUSTOMER_EMAIL)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertEqual(1, len(app_data.not_assigned_packages))
        self.assertIn(package, route.assigned_packages)

    def test_create_package_appendsAndReturnsCorrectly(self):
        app_data = ApplicationData()
        self.assertIsInstance(app_data.create_package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                                      td.VALID_CUSTOMER_EMAIL), Package)
        self.assertEqual(1, len(app_data.packages))

    def test_create_route_appendsAndReturnsCorrectly(self):
        app_data = ApplicationData()
        self.assertIsInstance(app_data.create_route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT), Route)
        self.assertEqual(1, len(app_data.routes))

    def test_find_package_by_id_whenNoPackages(self):
        app_data = ApplicationData()
        self.assertIsNone(app_data.find_package_by_id(td.INVALID_PACKAGE_ID))

    def test_find_package_by_id_invalidID(self):
        app_data = ApplicationData()
        app_data.create_package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                td.VALID_CUSTOMER_EMAIL)
        self.assertIsNone(app_data.find_package_by_id(td.INVALID_PACKAGE_ID))

    def test_find_package_by_id_returnsCorrectly(self):
        app_data = ApplicationData()
        package = app_data.create_package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                td.VALID_CUSTOMER_EMAIL)
        valid_id = package.id
        self.assertEqual(package, app_data.find_package_by_id(valid_id))

    def test_find_route_by_id_whenNoRoutes(self):
        app_data = ApplicationData()
        self.assertIsNone(app_data.find_route_by_id(td.INVALID_ROUTE_ID))

    def test_find_route_by_id_invalidID(self):
        app_data = ApplicationData()
        app_data.create_route(td.VALID_LOCATIONS_OUTPUT, td.VALID_DEPARTURE_TIME_INPUT)
        self.assertIsNone(app_data.find_route_by_id(td.INVALID_ROUTE_ID))

    def test_find_route_by_id_returnsCorrectly(self):
        app_data = ApplicationData()
        route = app_data.create_route(td.VALID_LOCATIONS_OUTPUT, td.VALID_DEPARTURE_TIME_INPUT)
        valid_id = route.id
        self.assertEqual(route, app_data.find_route_by_id(valid_id))

    def test_find_truck_by_id_invalidID(self):
        app_data = ApplicationData()
        self.assertIsNone(app_data.find_truck_by_id(td.INVALID_ROUTE_ID))

    # To be implemented further when Trucks class is ready
    def test_find_truck_by_id_returnsCorrectly(self):
        app_data = ApplicationData()
        truck = app_data.trucks[0]
        self.assertIsNone(truck, app_data.find_truck_by_id(truck.id))

    @patch("builtins.print")
    def test_create_employee_whenUsernameExists(self, mock_print):
        app_data = ApplicationData()
        app_data.create_employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                                 td.VALID_EMPLOYEE_ROLE)
        app_data.create_employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                                 td.VALID_EMPLOYEE_ROLE)
        mock_print.assert_called_with(f"Employee {td.VALID_USERNAME} already exist. Choose a different username!")

    def test_create_employee_appendsAndReturnsCorrectly(self):
        app_data = ApplicationData()

        self.assertIsInstance(app_data.create_employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME,
                                                       td.VALID_PASSWORD, td.VALID_EMPLOYEE_ROLE), Employee)
        self.assertEqual(1, len(app_data.employees))

    @patch("builtins.print")
    def test_find_employee_by_username_whenNoEmployees(self, mock_print):
        app_data = ApplicationData()
        found_employee = app_data.find_employee_by_username(td.VALID_USERNAME)
        mock_print.assert_called_with(f"There is no employee with username {td.VALID_USERNAME}!")
        self.assertIsNone(found_employee)

    @patch("builtins.print")
    def test_find_employee_by_username_invalidUsername(self, mock_print):
        app_data = ApplicationData()
        app_data.create_employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                                 td.VALID_EMPLOYEE_ROLE)
        found_employee = app_data.find_employee_by_username(td.INVALID_USERNAME)
        mock_print.assert_called_with(f"There is no employee with username {td.INVALID_USERNAME}!")
        self.assertIsNone(found_employee)

    def test_find_employee_by_username_returnsCorrectly(self):
        app_data = ApplicationData()
        employee = Employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                            td.VALID_EMPLOYEE_ROLE)
        app_data._employees.append(employee)
        self.assertEqual(employee, app_data.find_employee_by_username(td.VALID_USERNAME))

    @patch("builtins.print")
    def test_login_invalidEmployee(self, mock_print):
        app_data = ApplicationData()
        app_data.login(td.INVALID_EMPLOYEE)
        mock_print.assert_called_with("Invalid employee")

    def test_login_assignsCorrectly(self):
        app_data = ApplicationData()
        employee = Employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                            td.VALID_EMPLOYEE_ROLE)
        app_data.login(employee)
        self.assertEqual(employee, app_data.logged_in_employee)

    def test_logout_whenNotLoggedIn(self):
        app_data = ApplicationData()
        app_data.logout()
        self.assertIsNone(app_data.logged_in_employee)

    def test_logout_whenLoggedIn(self):
        app_data = ApplicationData()
        employee = Employee(td.VALID_USERNAME, td.VALID_FIRST_NAME, td.VALID_LAST_NAME, td.VALID_PASSWORD,
                            td.VALID_EMPLOYEE_ROLE)
        app_data.login(employee)
        app_data.logout()
        self.assertIsNone(app_data.logged_in_employee)

    def test_get_packages_by_assigned_status_whenNoPackages(self):
        app_data = ApplicationData()
        self.assertEqual([], app_data.get_packages_by_assigned_status(True))
        self.assertEqual([], app_data.get_packages_by_assigned_status(False))

    # To be further implemented when Package class is ready
    def test_get_packages_by_assigned_status_whenIsAssigned(self):
        app_data = ApplicationData()
        not_assigned_package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                       td.VALID_CUSTOMER_EMAIL)
        assigned_package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                   td.VALID_CUSTOMER_EMAIL)
        app_data._packages.append(assigned_package)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.assign_package(assigned_package)
        self.assertEqual([assigned_package], app_data.get_packages_by_assigned_status(True))

    # To be further implemented when Package class is ready
    def test_get_packages_by_assigned_status_whenNotAssigned(self):
        app_data = ApplicationData()
        not_assigned_package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                       td.VALID_CUSTOMER_EMAIL)
        assigned_package = Package(td.VALID_START_LOCATION, td.VALID_END_LOCATION, td.VALID_WEIGHT,
                                   td.VALID_CUSTOMER_EMAIL)
        app_data._packages.append(assigned_package)
        route = Route(td.VALID_LOCATIONS_INPUT, td.VALID_DEPARTURE_TIME_INPUT)
        route.assign_package(assigned_package)
        self.assertEqual([not_assigned_package], app_data.get_packages_by_assigned_status(False))


