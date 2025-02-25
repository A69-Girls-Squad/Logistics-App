from commands.show_employees import ShowEmployeesCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData
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
from commands.show_routes import ShowRoutesCommand
from commands.show_trucks import ShowTrucksCommand
from commands.unassign_package_from_route import UnassignPackageFromRouteCommand
import interface_menu


class CommandFactory:
    """
    Factory class responsible for creating command instances based on user input.

    The CommandFactory parses user input, identifies the corresponding command,
    and returns an instance of the appropriate command class. It uses shared
    application data to initialize commands.

    Attributes:
        _app_data (ApplicationData): The application data shared across commands.
    """

    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_command: str):
        """
        Creates and returns the appropriate command object based on user input.

        Args:
            input_command (str): A string containing the command and its parameters.

        Returns:
            Command: An instance of the corresponding command class.

        Raises:
            ApplicationError: If the command is not recognized or is invalid.
        """
        cmd = input_command
        params = []

        if cmd == "1":
            print(interface_menu.REGISTER_EMPLOYEE_MENU)
            params = [input("Username: "),
                      input("First Name: "),
                      input("Last Name: "),
                      input("Password: "),
                      input("Employee Role /Regular, Supervisor, Manager/: ")]
            return RegisterEmployeeCommand(params, self._app_data)

        if cmd == "2":
            print(interface_menu.LOGIN_MENU)
            params = [input("Username: "), input("Password: ")]
            return LoginCommand(params, self._app_data)

        if cmd == "3":
            return LogoutCommand(params, self._app_data)

        if cmd == "4":
            print(interface_menu.CREATE_ROUTE_MENU)
            params = [input("List of Locations /separated by comma/: "),
                      input("Departure Time /format YYYY-MM-DD HH:MM/: ")]
            return CreateRouteCommand(params, self._app_data)

        if cmd == "5":
            print(interface_menu.CREATE_PACKAGE_MENU)
            params = [input("Start Location: "),
                      input("End Location: "),
                      input("Weight: "),
                      input("Customer Email: ")]
            return CreatePackageCommand(params, self._app_data)

        if cmd == "6":
            print(interface_menu.SEARCH_ROUTE_MENU)
            params = [input("Please, enter the ID of the Package you need a Route for: ")]
            return SearchRouteCommand(params, self._app_data)

        if cmd == "7":
            print(interface_menu.SEARCH_TRUCK_MENU)
            params = [input("Please, enter the ID of the Route you need a Truck for: ")]
            return SearchTruckCommand(params, self._app_data)

        if cmd == "8":
            print(interface_menu.ASSIGN_TRUCK_TO_ROUTE_MENU)
            params = [input("Truck ID: "),
                      input("Route ID: ")]
            return AssignTruckToRouteCommand(params, self._app_data)

        if cmd == "9":
            print(interface_menu.REMOVE_TRUCK_MENU)
            params = [input("Truck ID: ")]
            return RemoveTruckFromRouteCommand(params, self._app_data)

        if cmd == "10":
            print(interface_menu.ASSIGN_PACKAGE_TO_ROUTE_MENU)
            params = [input("Package ID: "),
                      input("Route ID: ")]
            return AssignPackageToRouteCommand(params, self._app_data)

        if cmd == "11":
            print(interface_menu.BULK_ASSIGN_PACKAGES_MENU)
            params = [input("Route ID: "),
                      input("Package IDs /separated by comma/: ").split(",")]
            return BulkAssignPackagesCommand(params, self._app_data)

        if cmd == "12":
            print(interface_menu.REASSIGN_PACKAGE_MENU)
            params = [input("Package ID: "),
                      input("New Route ID: ")]
            return ReassignPackageCommand(params, self._app_data)

        if cmd == "13":
            print(interface_menu.REMOVE_PACKAGE_MENU)
            params = [input("Package ID: ")]
            return UnassignPackageFromRouteCommand(params, self._app_data)

        if cmd == "14":
            return ShowEmployeesCommand(params, self._app_data)

        if cmd == "15":
            print(interface_menu.SHOW_PACKAGE)
            params = [input("Package ID: ")]
            return ShowPackageCommand(params, self._app_data)

        if cmd == "16":
            print(interface_menu.SHOW_PACKAGES_MENU)
            params = [input("Status: ")]
            return ShowPackagesCommand(params, self._app_data)

        if cmd == "17":
            print(interface_menu.SHOW_ROUTE_MENU)
            params = [input("Route ID: ")]
            return ShowRouteCommand(params, self._app_data)

        if cmd == "18":
            print(interface_menu.SHOW_ROUTES_MENU)
            params = [input("Status: ")]
            return ShowRoutesCommand(params, self._app_data)

        if cmd == "19":
            return ShowTrucksCommand(params, self._app_data)

        if cmd.split()[0].lower() == "settime":
            parts = cmd.split()
            params = [" ".join(parts[1:])]
            return SetTimeCommand(params, self._app_data)

        raise ApplicationError(f"Command {cmd} is not supported.")
