import unittest
from unittest.mock import patch
from core.application_data import ApplicationData
from core.command_factory import CommandFactory
from errors.application_error import ApplicationError
from commands.assign_package_to_route import AssignPackageToRouteCommand
from commands.assign_truck_to_route import AssignTruckToRouteCommand
from commands.bulk_assign_packages import BulkAssignPackagesCommand
from commands.create_package import CreatePackageCommand
from commands.create_route import CreateRouteCommand
from commands.login import LoginCommand
from commands.logout import LogoutCommand
from commands.reassign_package import ReassignPackageCommand
from commands.register_employee import RegisterEmployeeCommand
from commands.remove_truck_from_route import RemoveTruckFromRouteCommand
from commands.search_route import SearchRouteCommand
from commands.search_truck import SearchTruckCommand
from commands.set_time import SetTimeCommand
from commands.show_package import ShowPackageCommand
from commands.show_packages import ShowPackagesCommand
from commands.show_route import ShowRouteCommand
from commands.show_trucks import ShowTrucksCommand
from commands.unassign_package_from_route import UnassignPackageFromRouteCommand


class CommandFactoryTests(unittest.TestCase):
    def setUp(self):
        self.data = ApplicationData()
        self.factory = CommandFactory(self.data)

    def test_properties_returnCorrectTypes(self):
        # Assert
        self.assertIsInstance(self.factory._app_data, ApplicationData)

    @patch("builtins.input", side_effect=["username", "password"])
    def test_create_withLogin_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("2")

        # Assert
        self.assertIsInstance(command, LoginCommand)
        self.assertEqual(list(command.params), ["username", "password"])

    def test_create_withLogout_createsInstance(self):
        # Act
        command = self.factory.create("3")

        # Assert
        self.assertIsInstance(command, LogoutCommand)
        self.assertEqual(list(command.params), [])

    @patch("builtins.input", side_effect=["user", "John", "Doe", "pass", "Manager"])
    def test_create_withRegisterEmployee_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("1")

        # Assert
        self.assertIsInstance(command, RegisterEmployeeCommand)
        self.assertEqual(list(command.params), ["user", "John", "Doe", "pass", "Manager"])

    @patch("builtins.input", side_effect=["loc1,loc2", "2023-10-10 10:00"])
    def test_create_withCreateRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("4")

        # Assert
        self.assertIsInstance(command, CreateRouteCommand)
        self.assertEqual(list(command.params), ["loc1,loc2", "2023-10-10 10:00"])

    @patch("builtins.input", side_effect=["loc1", "loc2", "10", "test@example.com"])
    def test_create_withCreatePackage_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("5")

        # Assert
        self.assertIsInstance(command, CreatePackageCommand)
        self.assertEqual(list(command.params), ["loc1", "loc2", "10", "test@example.com"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withSearchRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("6")

        # Assert
        self.assertIsInstance(command, SearchRouteCommand)
        self.assertEqual(list(command.params), ["1"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withSearchTruck_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("7")

        # Assert
        self.assertIsInstance(command, SearchTruckCommand)
        self.assertEqual(list(command.params), ["1"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withShowPackage_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("15")

        # Assert
        self.assertIsInstance(command, ShowPackageCommand)
        self.assertEqual(list(command.params), ["1"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withShowPackages_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("16")

        # Assert
        self.assertIsInstance(command, ShowPackagesCommand)
        self.assertEqual(list(command.params), ["1"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withShowRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("17")

        # Assert
        self.assertIsInstance(command, ShowRouteCommand)
        self.assertEqual(list(command.params), ["1"])

    def test_create_withShowTrucks_createsInstance(self):
        # Act
        command = self.factory.create("19")

        # Assert
        self.assertIsInstance(command, ShowTrucksCommand)
        self.assertEqual(list(command.params), [])

    @patch("builtins.input", side_effect=["1", "2"])
    def test_create_withAssignPackageToRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("10")

        # Assert
        self.assertIsInstance(command, AssignPackageToRouteCommand)
        self.assertEqual(list(command.params), ["1", "2"])

    @patch("builtins.input", side_effect=["1", "2"])
    def test_create_withAssignTruckToRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("8")

        # Assert
        self.assertIsInstance(command, AssignTruckToRouteCommand)
        self.assertEqual(list(command.params), ["1", "2"])

    @patch("builtins.input", side_effect=["1", "2,3"])
    def test_create_withBulkAssignPackages_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("11")

        # Assert
        self.assertIsInstance(command, BulkAssignPackagesCommand)
        self.assertEqual(list(command.params), ["1", ["2", "3"]])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withRemoveTruckFromRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("9")

        # Assert
        self.assertIsInstance(command, RemoveTruckFromRouteCommand)
        self.assertEqual(list(command.params), ["1"])

    @patch("builtins.input", side_effect=["1", "2"])
    def test_create_withReassignPackage_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("12")

        # Assert
        self.assertIsInstance(command, ReassignPackageCommand)
        self.assertEqual(list(command.params), ["1", "2"])

    @patch("builtins.input", side_effect=["1"])
    def test_create_withUnassignPackageFromRoute_createsInstance(self, mock_input):
        # Act
        command = self.factory.create("13")

        # Assert
        self.assertIsInstance(command, UnassignPackageFromRouteCommand)
        self.assertEqual(list(command.params), ["1"])

    def test_create_withSetTime_createsInstance(self):
        # Act
        command = self.factory.create("settime 2023-10-10 10:00")

        # Assert
        self.assertIsInstance(command, SetTimeCommand)
        self.assertEqual(list(command.params), ["2023-10-10 10:00"])

    def test_create_withInvalidCommand_raisesApplicationError(self):
        # Act & Assert
        with self.assertRaises(ApplicationError):
            self.factory.create("invalidcommand")