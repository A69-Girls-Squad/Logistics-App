import unittest
from unittest.mock import MagicMock
from commands.show_package import ShowPackageCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData


class ShowPackageCommandTests(unittest.TestCase):
    def setUp(self):
        # Arrange:
        self.mock_app_data = MagicMock(spec=ApplicationData)

        # Create a mock package to return when find_package_by_id is called
        self.mock_package = MagicMock()
        self.mock_package.id = 123
        self.mock_package.name = "Test Package"

        # Set up the mock behavior for find_package_by_id
        self.mock_app_data.find_package_by_id.return_value = self.mock_package

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = ShowPackageCommand([123], self.mock_app_data)

        # Assert
        self.assertEqual(command.params, (123,))
        self.assertEqual(command.app_data, self.mock_app_data)

    def test_execute_withValidPackageId_returnsPackageDetails(self):
        # Arrange
        command = ShowPackageCommand([123], self.mock_app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, str(self.mock_package))
        self.mock_app_data.find_package_by_id.assert_called_once_with(123)

    def test_execute_withInvalidPackageId_raisesApplicationError(self):
        # Arrange
        self.mock_app_data.find_package_by_id.return_value = None
        command = ShowPackageCommand([999], self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("No Package found!", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = ShowPackageCommand([123], self.mock_app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsOne(self):
        # Arrange
        command = ShowPackageCommand([123], self.mock_app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 1)
