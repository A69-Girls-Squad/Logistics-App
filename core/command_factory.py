from commands.assign_package_to_route import AssignPackageToRoute
from commands.assign_truck_to_route import AssignTruckToRouteCommand
from commands.bulk_assign_packages import BulkAssignPackagesCommand
from commands.create_package import CreatePackageCommand
from commands.create_route import CreateRouteCommand
from commands.remove_truck_from_route import RemoveTruckFromRouteCommand
from commands.search_route import SearchRouteCommand
from commands.search_truck import SearchTruckCommand
from commands.send_package_info_to_customer import SendPackageInfoToCustomerCommand
from commands.show_packages import ShowPackagesCommand
from commands.show_route import ShowRouteCommand
from commands.show_routes_inprogress import ShowRoutesInProgressCommand
from commands.show_trucks import ShowTrucksCommand
from commands.show_unassigned_packages import ShowUnassignedPackagesCommand
from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line: str):
        cmd, *params = input_line.split()

        # if cmd.upper() == 'LOGIN':
        #     return LoginCommand(self._app_data)
        # if cmd.upper() == 'LOGOUT':
        #     return LogoutCommand(self._app_data)
        if cmd.lower() == 'createroute':
            return CreateRouteCommand(params, self._app_data)
        if cmd.lower() == 'createpackage':
            return CreatePackageCommand(params, self._app_data)
        if cmd.lower() == 'searchroute':
            return SearchRouteCommand(params, self._app_data)
        if cmd.lower() == 'searchtruck':
            return SearchTruckCommand(params, self._app_data)
        if cmd.lower() == 'showpackages':
            return ShowPackagesCommand(params, self._app_data)
        if cmd.lower() == 'showroute':
            return ShowRouteCommand(params, self._app_data)
        if cmd.lower() == 'showtrucks':
            return ShowTrucksCommand(params, self._app_data)
        if cmd.lower() == 'assignpackagetoroute':
            return AssignPackageToRoute(params, self._app_data)
        if cmd.lower() == 'assigntrucktoroute':
            return AssignTruckToRouteCommand(params, self._app_data)
        if cmd.lower() == 'bulkassignpackages':
            return BulkAssignPackagesCommand(params, self._app_data)
        if cmd.lower() == 'removetruckfromroute':
            return RemoveTruckFromRouteCommand(params, self._app_data)
        if cmd.lower() == 'sendpackageinfotocustomer':
            return SendPackageInfoToCustomerCommand(params, self._app_data)
        if cmd.lower() == 'showroutesinprogress':
            return ShowRoutesInProgressCommand(params, self._app_data)
        if cmd.lower() == 'showunassignedpackages':
            return ShowUnassignedPackagesCommand(params, self._app_data)

        raise ValueError(f"Command {cmd} is not supported.")