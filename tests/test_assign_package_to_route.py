import unittest
from commands.assign_package_to_route import AssignPackageToRouteCommand
from errors.application_error import ApplicationError


class ApplicationData:
    def __init__(self):
        self.has_logged_in_employee = True
        self.logged_in_employee = "test_user"
        self.packages = {}
        self.routes = {}

    def assign_package_to_route(self, package_id, route_id):
        if package_id not in self.packages:
            raise ApplicationError(f"Package with ID {package_id} does not exist.")
        if route_id not in self.routes:
            raise ApplicationError(f"Route with ID {route_id} does not exist.")
        self.packages[package_id] = route_id

class AssignPackageToRouteCommandTests(unittest.TestCase):
    def setUp(self):

        self.app_data = ApplicationData()
        self.app_data.packages = {1: None, 2: None}
        self.app_data.routes = {101: None, 102: None}
        self.params = ["1", "101"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = AssignPackageToRouteCommand(self.params, self.app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.app_data)

    def test_execute_withValidPackageAndRoute_assignsPackageAndReturnsMessage(self):
        # Arrange
        command = AssignPackageToRouteCommand(self.params, self.app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, "Package with ID 1 was assigned to Route with ID 101")
        self.assertEqual(self.app_data.packages[1], 101)

    def test_execute_withInvalidPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "999"
        command = AssignPackageToRouteCommand([invalid_package_id, "101"], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn(f"Package with ID {invalid_package_id} does not exist.", str(context.exception))

    def test_execute_withInvalidRouteId_raisesApplicationError(self):
        # Arrange
        invalid_route_id = "999"
        command = AssignPackageToRouteCommand(["1", invalid_route_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn(f"Route with ID {invalid_route_id} does not exist.", str(context.exception))

    def test_execute_withNonIntegerPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "invalid"
        command = AssignPackageToRouteCommand([invalid_package_id, "101"], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withNonIntegerRouteId_raisesApplicationError(self):
        # Arrange
        invalid_route_id = "invalid"
        command = AssignPackageToRouteCommand(["1", invalid_route_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = ["1"]
        command = AssignPackageToRouteCommand(insufficient_params, self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = AssignPackageToRouteCommand(self.params, self.app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsTwo(self):
        # Arrange
        command = AssignPackageToRouteCommand(self.params, self.app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 2)
