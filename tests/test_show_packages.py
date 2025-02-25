import unittest
from commands.show_package import ShowPackageCommand
from errors.application_error import ApplicationError


class ApplicationData:
    def __init__(self):
        self.has_logged_in_employee = True
        self.logged_in_employee = "test_user"
        self.packages = []

    def find_package_by_id(self, package_id):
        for package in self.packages:
            if package["id"] == package_id:
                return package
        return None

class ShowPackageCommandTests(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()
        self.test_package = {"id": 1, "start_location": "SYD", "end_location": "MEL", "weight": 45.5, "customer_email": "customer@example.com"}
        self.app_data.packages.append(self.test_package)
        self.params = ["1"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = ShowPackageCommand(self.params, self.app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.app_data)

    def test_execute_withValidPackageId_returnsPackageString(self):
        # Arrange
        command = ShowPackageCommand(self.params, self.app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, str(self.test_package))

    def test_execute_withInvalidPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "999"
        command = ShowPackageCommand([invalid_package_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("No Package found!", str(context.exception))

    def test_execute_withNonIntegerPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "invalid"
        command = ShowPackageCommand([invalid_package_id], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = []
        command = ShowPackageCommand(insufficient_params, self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = ShowPackageCommand(self.params, self.app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsOne(self):
        # Arrange
        command = ShowPackageCommand(self.params, self.app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 1)

