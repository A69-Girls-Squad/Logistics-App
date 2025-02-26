import unittest
from unittest.mock import Mock

from commands.base_command import BaseCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole
from commands.login import LoginCommand


def _create_fake_params(
        *,
        username="username",
        password="password1234"):
    return [username, password]


class LoginCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        cmd = LoginCommand(["a"] * 1, Mock())
        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_initializer_raisesError_tooManyParamsCount(self):
        cmd = LoginCommand(["a"] * 3, Mock())
        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_initializer_passes_validParamsCount(self):
        LoginCommand(["a"] * 2, Mock())

    def test_execute_logsIn_validParams(self):
        fake_params = _create_fake_params()
        app_data = ApplicationData()
        app_data.create_employee("username", "John", "Smith", "password1234", EmployeeRole.REGULAR)
        cmd = LoginCommand(fake_params, app_data)

        output = cmd.execute()

        self.assertEqual(f"Employee username successfully logged in!", output)

    def test_execute_raisesError_invalidUsername(self):
        from errors.application_error import ApplicationError
        fake_params = _create_fake_params(username="invalidUsername")
        app_data = ApplicationData()
        app_data.create_employee("username", "John", "Smith", "password1234", EmployeeRole.REGULAR)
        cmd = LoginCommand(fake_params, app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_execute_raisesError_invalidPassword(self):
        fake_params = _create_fake_params(password="invalidPassword")
        app_data = ApplicationData()
        app_data.create_employee("username", "John", "Smith", "password1234", EmployeeRole.REGULAR)
        cmd = LoginCommand(fake_params, app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_execute_raisesError_whenNoEmployees(self):
        fake_params = _create_fake_params()
        app_data = ApplicationData()
        cmd = LoginCommand(fake_params, app_data)

        with self.assertRaises(ApplicationError):
            cmd.execute()
