
from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.core.application_data import ApplicationData
from skeleton.models.constants.assign_status import AssignStatus


class ShowPackagesCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        status = self.params[0]

        if status == AssignStatus.ASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(True)
        elif status == AssignStatus.UNASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(False)
        else:
            packages = self.app_data.packages

        return str(packages)


