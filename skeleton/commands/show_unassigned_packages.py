from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.core.application_data import ApplicationData
from skeleton.models.package import Package


class ShowUnassignedPackagesCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        unassigned_packages = []
        for package in self._app_data.packages:
            if package.status == Package.STATUS.UNASSIGNED:
                unassigned_packages.append(package)
        return f"Routs In Progress:\n"+"\n".join(unassigned_packages)