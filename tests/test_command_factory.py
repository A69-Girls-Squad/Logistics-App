import unittest
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
from commands.send_package_info_to_customer import SendPackageInfoToCustomerCommand
from commands.set_time import SetTimeCommand
from commands.show_package import ShowPackageCommand
from commands.show_packages import ShowPackagesCommand
from commands.show_route import ShowRouteCommand
from commands.show_routes_inprogress import ShowRoutesInProgressCommand
from commands.show_trucks import ShowTrucksCommand
from commands.unassign_package_from_route import UnassignPackageToRouteCommand


class CommandFactoryTests(unittest.TestCase):
    def test_properties_returnCorrectTypes(self):
        # Arrange
        data = ApplicationData()

        # Act
        factory = CommandFactory(data)

        # Assert
        self.assertIsInstance(factory._app_data, ApplicationData)

    def test_create_withLogin_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("login param1 param2")

        # Assert
        self.assertIsInstance(command, LoginCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 2)

    def test_create_withLogout_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("logout")

        # Assert
        self.assertIsInstance(command, LogoutCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 0)

    def test_create_withRegisterEmployee_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("registeremployee param1 param2 param3 param4")

        # Assert
        self.assertIsInstance(command, RegisterEmployeeCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 4)

    def test_create_withCreateRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("createroute param1 param2")

        # Assert
        self.assertIsInstance(command, CreateRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 2)

    def test_create_withCreatePackage_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("createpackage param1 param2 param3 param4")

        # Assert
        self.assertIsInstance(command, CreatePackageCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 4)

    def test_create_withSearchRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("searchroute param")

        # Assert
        self.assertIsInstance(command, SearchRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withSearchTruck_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("searchtruck param")

        # Assert
        self.assertIsInstance(command, SearchTruckCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withShowPackages_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("showpackages param")

        # Assert
        self.assertIsInstance(command, ShowPackagesCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withShowPackage_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("showpackage param")

        # Assert
        self.assertIsInstance(command, ShowPackageCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withShowRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("showroute param")

        # Assert
        self.assertIsInstance(command, ShowRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withShowTrucks_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("showtrucks")

        # Assert
        self.assertIsInstance(command, ShowTrucksCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 0)

    def test_create_withAssignPackageToRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("assignpackagetoroute param1 param2")

        # Assert
        self.assertIsInstance(command, AssignPackageToRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 2)

    def test_create_withAssignTruckToRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("assigntrucktoroute param")

        # Assert
        self.assertIsInstance(command, AssignTruckToRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withBulkAssignPackages_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("bulkassignpackages param1 param2")

        # Assert
        self.assertIsInstance(command, BulkAssignPackagesCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 2)

    def test_create_withRemoveTruckFromRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("removetruckfromroute param")

        # Assert
        self.assertIsInstance(command, RemoveTruckFromRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withSendPackageInfoToCustomer_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("sendpackageinfotocustomer param")

        # Assert
        self.assertIsInstance(command, SendPackageInfoToCustomerCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withShowRoutesInProgress_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("showroutesinprogress")

        # Assert
        self.assertIsInstance(command, ShowRoutesInProgressCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 0)

    def test_create_withUnassignPackageToRoute_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("unassignpackagetoroute param1 param2")

        # Assert
        self.assertIsInstance(command, UnassignPackageToRouteCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 2)

    def test_create_withReassignPackage_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("reassignpackage param1 param2 param3")

        # Assert
        self.assertIsInstance(command, ReassignPackageCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 3)

    def test_create_withSetTime_createsInstance(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act
        command = factory.create("settime param")

        # Assert
        self.assertIsInstance(command, SetTimeCommand)
        self.assertIsInstance(command.app_data, ApplicationData)
        self.assertEqual(len(command.params), 1)

    def test_create_withInvalidCommand_raisesApplicationError(self):
        # Arrange
        data = ApplicationData()
        factory = CommandFactory(data)

        # Act & Assert
        with self.assertRaises(ApplicationError):
            factory.create("invalidcommand param")
