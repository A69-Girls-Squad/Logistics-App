import unittest
from unittest.mock import MagicMock
from commands.show_employees import ShowEmployeesCommand
from errors.application_error import ApplicationError
from models.constants.employee_role import EmployeeRole


class ShowEmployeesCommandTests(unittest.TestCase):
    def setUp(self):
        # Arrange:
        self.mock_app_data = MagicMock()
        self.mock_app_data.has_logged_in_employee = True
        self.mock_app_data.logged_in_employee = MagicMock()

        self.mock_employee1 = MagicMock()
        self.mock_employee1.username = "user1"
        self.mock_employee1.employee_role = EmployeeRole.MANAGER

        self.mock_employee2 = MagicMock()
        self.mock_employee2.username = "user2"
        self.mock_employee2.employee_role = EmployeeRole.REGULAR

        self.mock_app_data.employees = []

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Assert
        self.assertEqual(command.params, tuple([]))
        self.assertEqual(command.app_data, self.mock_app_data)

    def test_execute_withManagerRole_returnsEmployeeList(self):
        # Arrange
        self.mock_app_data.logged_in_employee = self.mock_employee1  # Set logged-in user as manager
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Act
        result = command.execute()

        # Assert
        expected_output = (
            "--EMPLOYEES--\n"
            "1. user1 (EmployeeRole.MANAGER)\n"
            "2. user2 (EmployeeRole.REGULAR)"
        )
        self.assertEqual(result, expected_output)

    def test_execute_withNonManagerRole_raisesApplicationError(self):
        # Arrange
        self.mock_app_data.logged_in_employee = self.mock_employee2
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("You are not a Manager!", str(context.exception))

    def test_execute_withNoEmployees_returnsEmptyList(self):
        # Arrange
        self.mock_app_data.logged_in_employee = self.mock_employee1  # Mock logged-in employee
        self.mock_app_data.employees = []  # Ensure employees list is empty
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Act
        result = command.execute()

        # Debug
        print(f"Result: {result}")

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsZero(self):
        # Arrange
        command = ShowEmployeesCommand([], self.mock_app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 0)
