from commands.create_package import CreatePackageCommand
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
        if cmd.upper() == 'createroute':
            return
        if cmd.upper() == 'createpackage':
            return CreatePackageCommand(self._app_data)
        if cmd.upper() == 'searchroute':
            return
        if cmd.upper() == 'searchtruck':
            return
        if cmd.upper() == 'showpackages':
            return
        if cmd.upper() == 'showroute':
            return
        if cmd.upper() == 'showtrucks':
            return
        if cmd.upper() == 'assignpackagetoroute':
            return
        if cmd.upper() == 'assigntrucktoroute':
            return
        if cmd.upper() == 'sendpackageinfotocustomer':
            return
        raise ValueError(f"Command {cmd} is not supported.")