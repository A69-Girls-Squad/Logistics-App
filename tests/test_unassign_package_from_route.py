import unittest

from commands.unassign_package_from_route import UnassignPackageFromRouteCommand
from errors.application_error import ApplicationError


class Package:
    def __init__(self, package_id, route_id=None):
        self.id = package_id
        self.route_id = route_id

class ApplicationData:
    def __init__(self):
        self.has_logged_in_employee = True
        self.logged_in_employee = "test_user"
        self.packages = []

    def find_package_by_id(self, package_id):
        for package in self.packages:
            if package.id == package_id:
                return package
        return None

    def unassign_package_from_route(self, package_id):
        package = self.find_package_by_id(package_id)
        if not package:
            raise ApplicationError(f"Package with ID {package_id} does not exist.")
        if not package.route_id:
            raise ApplicationError(f"Package with ID {package_id} is not assigned to any route.")
        package.route_id = None

class UnassignPackageFromRouteCommandTests(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()
        self.test_package = Package(1, route_id=101)
        self.app_data.packages.append(self.test_package)
        self.params = ["1"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = UnassignPackageFromRouteCommand(self.params, self.app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.app_data)

    def test_execute_withValidPackageId_unassignsPackageAndReturnsMessage(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, "Package with ID 1 was unassigned from Route with ID 101")
        self.assertIsNone(self.test_package.route_id)

    def test_execute_withInvalidPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "999"
        command = UnassignPackageFromRouteCommand([invalid_package_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn(f"Package with ID {invalid_package_id} does not exist.", str(context.exception))

    def test_execute_withUnassignedPackage_raisesApplicationError(self):
        # Arrange
        unassigned_package = Package(2)
        self.app_data.packages.append(unassigned_package)
        command = UnassignPackageFromRouteCommand(["2"], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn(f"Package with ID 2 is not assigned to any route.", str(context.exception))

    def test_execute_withNonIntegerPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "invalid"
        command = UnassignPackageFromRouteCommand([invalid_package_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = []
        command = UnassignPackageFromRouteCommand(insufficient_params, self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsOne(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 1)
