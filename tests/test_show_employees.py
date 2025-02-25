import unittest
from commands.show_employees import ShowEmployeesCommand
from errors.application_error import ApplicationError
from models.constants.employee_role import EmployeeRole


class Employee:
    def __init__(self, username, employee_role):
        self.username = username
        self.employee_role = employee_role

    def __str__(self):
        return f"{self.username} ({self.employee_role})"

class ApplicationData:
    def __init__(self):
        self.has_logged_in_employee = True
        self.logged_in_employee = None
        self.employees = []

class ShowEmployeesCommandTests(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()
        self.employee1 = Employee("user1", EmployeeRole.MANAGER)
        self.employee2 = Employee("user2", EmployeeRole.REGULAR)
        self.app_data.employees = [self.employee1, self.employee2]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = ShowEmployeesCommand([], self.app_data)

        # Assert
        self.assertEqual(command.params, tuple([]))
        self.assertEqual(command.app_data, self.app_data)

    def test_execute_withManagerRole_returnsEmployeeList(self):
        # Arrange
        self.app_data.logged_in_employee = self.employee1  # Set logged-in user as manager
        command = ShowEmployeesCommand([], self.app_data)

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
        self.app_data.logged_in_employee = self.employee2
        command = ShowEmployeesCommand([], self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("You are not a Manager!", str(context.exception))

    def test_execute_withNoEmployees_returnsEmptyList(self):
        # Arrange
        self.app_data.logged_in_employee = self.employee1
        self.app_data.employees = []
        command = ShowEmployeesCommand([], self.app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertEqual(result, None) #--EMPLOYEES--

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = ShowEmployeesCommand([], self.app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsZero(self):
        # Arrange
        command = ShowEmployeesCommand([], self.app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 0)