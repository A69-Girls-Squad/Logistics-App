from core.application_data import ApplicationData


class CommandFactory:
    def __init__(self, data: ApplicationData):
        self._app_data = data

    def create(self, input_line: str):
        cmd, *params = input_line.split()

    # if cmd.lower() == "createcategory":
    #     return CreateCategoryCommand(params, self._app_data)
    #
    # raise ValueError(f"Command {cmd} is not supported.")