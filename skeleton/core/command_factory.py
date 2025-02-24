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
from commands.send_package_info_to_customer import SendPackageInfoToCustomerCommand
from commands.set_time import SetTimeCommand
from commands.show_package import ShowPackageCommand
from commands.show_packages import ShowPackagesCommand
from commands.show_route import ShowRouteCommand
from commands.show_routes_inprogress import ShowRoutesInProgressCommand
from commands.show_trucks import ShowTrucksCommand
from commands.unassign_package_from_route import UnassignPackageToRouteCommand


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

    def create(self, input_line: str):
        """
        Creates and returns the appropriate command object based on user input.

        Args:
            input_line (str): A string containing the command and its parameters.

        Returns:
            Command: An instance of the corresponding command class.

        Raises:
            ApplicationError: If the command is not recognized or is invalid.
        """
        cmd, *params = input_line.split()

        if cmd.lower() == "login":
            return LoginCommand(params, self._app_data)
        if cmd.lower() == "logout":
            return LogoutCommand(params, self._app_data)
        if cmd.lower() == "registeremployee":
            return RegisterEmployeeCommand(params, self._app_data)
        if cmd.lower() == "createroute":
            return CreateRouteCommand(params, self._app_data)
        if cmd.lower() == "createpackage":
            return CreatePackageCommand(params, self._app_data)
        if cmd.lower() == "searchroute":
            return SearchRouteCommand(params, self._app_data)
        if cmd.lower() == "searchtruck":
            return SearchTruckCommand(params, self._app_data)
        if cmd.lower() == "showpackages":
            return ShowPackagesCommand(params, self._app_data)
        if cmd.lower() == "showpackage":
            return ShowPackageCommand(params, self._app_data)
        if cmd.lower() == "showroute":
            return ShowRouteCommand(params, self._app_data)
        if cmd.lower() == "showtrucks":
            return ShowTrucksCommand(params, self._app_data)
        if cmd.lower() == "assignpackagetoroute":
            return AssignPackageToRouteCommand(params, self._app_data)
        if cmd.lower() == "assignpackagetoroute":
            return AssignPackageToRouteCommand(params, self._app_data)
        if cmd.lower() == "assigntrucktoroute":
            return AssignTruckToRouteCommand(params, self._app_data)
        if cmd.lower() == "bulkassignpackages":
            return BulkAssignPackagesCommand(params, self._app_data)
        if cmd.lower() == "removetruckfromroute":
            return RemoveTruckFromRouteCommand(params, self._app_data)
        if cmd.lower() == "sendpackageinfotocustomer":
            return SendPackageInfoToCustomerCommand(params, self._app_data)
        if cmd.lower() == "showroutesinprogress":
            return ShowRoutesInProgressCommand(params, self._app_data)
        if cmd.lower() == "unassignpackagetoroute":
            return UnassignPackageToRouteCommand(params, self._app_data)
        if cmd.lower() == "reassignpackage":
            return ReassignPackageCommand(params, self._app_data)
        if cmd.lower() == "settime":
            return SetTimeCommand(params, self._app_data)

        raise ApplicationError(f"Command {cmd} is not supported.")
