from skeleton.commands.assign_package_to_route import AssignPackageToRoute
from skeleton.commands.assign_truck_to_route import AssignTruckToRouteCommand
from skeleton.commands.bulk_assign_packages import BulkAssignPackagesCommand
from skeleton.commands.create_package import CreatePackageCommand
from skeleton.commands.create_route import CreateRouteCommand
from skeleton.commands.login import LoginCommand
from skeleton.commands.logout import LogoutCommand
from skeleton.commands.register_employee import RegisterEmployeeCommand
from skeleton.commands.remove_truck_from_route import RemoveTruckFromRouteCommand
from skeleton.commands.search_route import SearchRouteCommand
from skeleton.commands.search_truck import SearchTruckCommand
from skeleton.commands.send_package_info_to_customer import SendPackageInfoToCustomerCommand
from skeleton.commands.show_packages import ShowPackagesCommand
from skeleton.commands.show_route import ShowRouteCommand
from skeleton.commands.show_routes_inprogress import ShowRoutesInProgressCommand
from skeleton.commands.show_trucks import ShowTrucksCommand
from skeleton.core.application_data import ApplicationData



class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line: str):
        cmd, *params = input_line.split()

        if cmd.lower() == 'login':
            return LoginCommand(params, self._app_data)
        if cmd.lower() == 'logout':
            return LogoutCommand(params, self._app_data)
        if cmd.lower() == 'registeremployee':
            return RegisterEmployeeCommand(params, self._app_data)
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

        raise ValueError(f"Command {cmd} is not supported.")
