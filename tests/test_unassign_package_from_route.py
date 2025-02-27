import unittest
from unittest.mock import MagicMock
from commands.unassign_package_from_route import UnassignPackageFromRouteCommand
from errors.application_error import ApplicationError


class UnassignPackageFromRouteCommandTests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.app_data = None

    def setUp(self):
        self.mock_app_data = MagicMock()
        self.mock_app_data.has_logged_in_employee = True
        self.mock_app_data.logged_in_employee = "test_user"

        self.mock_package = MagicMock()
        self.mock_package.id = 1
        self.mock_package.route_id = 101

        self.mock_app_data.packages = [self.mock_package]

        self.mock_app_data.find_package_by_id.return_value = self.mock_package

        self.params = ["1"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = UnassignPackageFromRouteCommand(self.params, self.mock_app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.mock_app_data)

    def test_execute_withValidPackageId_unassignsPackageAndReturnsMessage(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.mock_app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, "Package with ID 1 was unassigned from Route with ID 101")
        self.mock_package.route_id = None  # Mocked package's route_id should be set to None
        self.assertIsNone(self.mock_package.route_id)
        self.mock_app_data.unassign_package_from_route.assert_called_once_with(1)

    def test_execute_withInvalidPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "999"
        self.mock_app_data.find_package_by_id.return_value = None  # Simulate package not found
        command = UnassignPackageFromRouteCommand([invalid_package_id], self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn(f"Package with ID {invalid_package_id} does not exist.", str(context.exception))


    def test_execute_withNonIntegerPackageId_raisesApplicationError(self):
        # Arrange
        invalid_package_id = "invalid"
        command = UnassignPackageFromRouteCommand([invalid_package_id], self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = []
        command = UnassignPackageFromRouteCommand(insufficient_params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.mock_app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsOne(self):
        # Arrange
        command = UnassignPackageFromRouteCommand(self.params, self.mock_app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 1)
