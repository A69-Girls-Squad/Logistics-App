import unittest
from unittest.mock import MagicMock
from commands.create_package import CreatePackageCommand
from errors.application_error import ApplicationError


class CreatePackageCommandTests(unittest.TestCase):
    def setUp(self):
        # Arrange:
        self.mock_app_data = MagicMock()
        self.mock_app_data.has_logged_in_employee = True
        self.mock_app_data.logged_in_employee = "test_user"
        self.mock_app_data.packages = []
        self.mock_app_data.next_package_id = 1
        mock_package = MagicMock()
        mock_package.id = 1
        mock_package.start_location = "SYD"
        mock_package.end_location = "MEL"
        mock_package.weight = 45.5
        mock_package.customer_email = "customer@example.com"

        self.mock_app_data.create_package.return_value = mock_package
        self.params = ["SYD", "MEL", "45.5", "customer@example.com"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = CreatePackageCommand(self.params, self.mock_app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.mock_app_data)

    def test_execute_withValidParameters_createsPackageAndReturnsMessage(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.mock_app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertIn("Package with ID 1 was created!", result)
        self.assertIn("Start Location: | SYD", result)
        self.assertIn("End Location:   | MEL", result)
        self.assertIn("Weight:         | 45.5 kg", result)
        self.assertIn("Customer email: | customer@example.com", result)
        self.mock_app_data.create_package.assert_called_once_with("SYD", "MEL", 45.5, "customer@example.com")

    def test_execute_withInvalidWeight_raisesApplicationError(self):
        # Arrange
        invalid_weight = "invalid"
        invalid_params = ["SYD", "MEL", invalid_weight, "customer@example.com"]
        command = CreatePackageCommand(invalid_params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = ["SYD", "MEL", "45.5"]
        command = CreatePackageCommand(insufficient_params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.mock_app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsFour(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.mock_app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 4)
