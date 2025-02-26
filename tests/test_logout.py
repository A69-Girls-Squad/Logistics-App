import unittest
from unittest.mock import Mock
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole
from commands.login import LoginCommand
from commands.logout import LogoutCommand


def _create_fake_params():
    return []


class LogoutCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooManyParamsCount(self):
        cmd = LogoutCommand(["a"] * 3, Mock())
        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_initializer_passes_validParamsCount(self):
        LogoutCommand(["a"] * 0, Mock())

    def test_execute_logsOut(self):
        fake_params = ["username", "password1234"]
        app_data = ApplicationData()
        app_data.create_employee("username", "John", "Smith", "password1234", EmployeeRole.REGULAR)
        LoginCommand(fake_params, app_data)
        fake_params = _create_fake_params()
        LogoutCommand(fake_params, app_data)

        self.assertIsNone(app_data.logged_in_employee)
