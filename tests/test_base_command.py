import unittest
from unittest.mock import MagicMock, patch
from commands.base_command import BaseCommand
from errors.application_error import ApplicationError


class BaseCommandTests(unittest.TestCase):
    def setUp(self):
        # Arrange:
        self.mock_app_data = MagicMock()
        self.mock_app_data.has_logged_in_employee = False
        self.mock_app_data.logged_in_employee = None
        self.params = ["param1", "param2"]

    def test_init_withValidArguments_createsInstance(self):
        # Arrange
        params = self.params
        app_data = self.mock_app_data

        # Act
        base_command = BaseCommand(params, app_data)

        # Assert
        self.assertEqual(base_command.params, tuple(params))
        self.assertEqual(base_command.app_data, app_data)
        self.assertIsNotNone(base_command.logger)

    def test_execute_withoutLoginRequired_returnsEmptyString(self):
        # Arrange
        class NoLoginCommand(BaseCommand):
            def _requires_login(self) -> bool:
                return False

            def _expected_params_count(self) -> int:
                return 2

        no_login_command = NoLoginCommand(self.params, self.mock_app_data)

        # Act
        result = no_login_command.execute()

        # Assert
        self.assertEqual(result, "")

    def test_execute_withLoginRequiredAndNotLoggedIn_raisesValueError(self):
        # Arrange
        class TestCommand(BaseCommand):
            def _requires_login(self) -> bool:
                return True

            def _expected_params_count(self) -> int:
                return 2

        test_command = TestCommand(self.params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            test_command.execute()
        self.assertIn("You are not logged in!", str(context.exception))

    def test_execute_withInvalidParameterCount_raisesApplicationError(self):
        # Arrange
        class InvalidParamCountCommand(BaseCommand):
            def _requires_login(self) -> bool:
                return False

            def _expected_params_count(self) -> int:
                return 3

        invalid_param_command = InvalidParamCountCommand(self.params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            invalid_param_command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_throw_if_employee_logged_in_withLoggedInEmployee_raisesValueError(self):
        # Arrange
        self.mock_app_data.has_logged_in_employee = True
        self.mock_app_data.logged_in_employee = MagicMock(username="test_user")
        base_command = BaseCommand(self.params, self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            base_command._throw_if_employee_logged_in()
        self.assertIn("is logged in!", str(context.exception))

    def test_throw_if_employee_logged_in_withNoLoggedInEmployee_doesNotRaise(self):
        # Arrange
        self.mock_app_data.has_logged_in_employee = False
        base_command = BaseCommand(self.params, self.mock_app_data)

        # Act & Assert
        try:
            base_command._throw_if_employee_logged_in()
        except ValueError:
            self.fail("_throw_if_employee_logged_in() raised ValueError unexpectedly!")