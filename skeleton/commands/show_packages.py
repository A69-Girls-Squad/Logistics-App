from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from core.application_time import ApplicationTime
from models.constants.assign_status import AssignStatus


class ShowPackagesCommand(BaseCommand):
    """
    Command to display a list of packages based on their assignment status.

    This command validates the input parameter, retrieves packages based on their status,
    and returns their string representations.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (a single status string: 'assigned', 'unassigned', or 'all').
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display packages based on their assignment status.

        Returns:
            str: A formatted string containing the details of the packages.

        Notes:
            - If the status is 'assigned', only assigned packages are displayed.
            - If the status is 'unassigned', only unassigned packages are displayed.
            - If the status is 'all', all packages are displayed.
        """
        status = self.params[0].lower()
    def execute(self):
        requested_status = self.params[0].lower()
        result = "PACKAGES:" + self.ROW_SEP

        if requested_status == AssignStatus.ASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(True)
        elif requested_status == AssignStatus.UNASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(False)
        else:
            packages = self.app_data.packages

        def status(package):
            if package.departure_time:
                if ApplicationTime.current() < package.departure_time:
                    status = f"\nPackage status: | Awaiting Dispatch\n{self.TABLE_SEP}"
                elif ApplicationTime.current() < package.estimated_arrival_time:
                    status = f"\nPackage status: | In Transit\n{self.TABLE_SEP}"
                else:
                    status = f"\nPackage status: | Delivered\n{self.TABLE_SEP}"
                status += (f"\nDeparture time: | {package.departure_time.isoformat(sep=" ", timespec="minutes")}\n{self.TABLE_SEP}"
                           f"\nArrival time:   | {package.estimated_arrival_time.isoformat(sep=" ", timespec="minutes")}\n{self.TABLE_SEP}")
            else:
                status = f"\nPackage status: | Not assigned\n{self.TABLE_SEP}"
            return status

        result += "\n".join([f"\nPACKAGE ID:     | {package.id}"
                            f"\n{self.TABLE_SEP}"
                            f"\nStart Location: | {package.start_location}"
                            f"\n{self.TABLE_SEP}"
                            f"\nEnd Location:   | {package.end_location}"
                            f"\n{self.TABLE_SEP}"
                            f"\nWeight:         | {package.weight:.2f} kg"
                            f"\n{self.TABLE_SEP}"
                            f"\nCustomer Email: | {package.customer_email}"
                            f"\n{self.TABLE_SEP}"
                            f"{status(package)}" + self.ROW_SEP for package in packages]) + self.ROW_SEP

        self.logger.info(result)
        return result



