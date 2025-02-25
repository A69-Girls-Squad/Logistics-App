from core.application_time import ApplicationTime
from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from models.constants.assign_status import AssignStatus


class ShowPackagesCommand(BaseCommand):
    """
    Command to display a list of packages based on their assignment status.

    This command validates the input parameter, retrieves packages based on their status,
    and returns their string representations.
    """
    def __init__(self, params, app_data: ApplicationData):
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
        super().execute()

        requested_status = self.params[0].lower()
        result = "PACKAGES:" + BaseCommand.ROW_SEP

        if requested_status == AssignStatus.ASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(True)
        elif requested_status == AssignStatus.UNASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(False)
        elif requested_status == AssignStatus.ALL:
            packages = self.app_data.packages
        else:
            raise ApplicationError("Invalid input!")

        def status_string(package):
            if package.departure_time:
                if ApplicationTime.current() < package.departure_time:
                    status = f"\nPackage status: | Awaiting Dispatch\n{BaseCommand.TABLE_SEP}"
                elif ApplicationTime.current() < package.estimated_arrival_time:
                    status = f"\nPackage status: | In Transit\n{BaseCommand.TABLE_SEP}"
                else:
                    status = f"\nPackage status: | Delivered\n{BaseCommand.TABLE_SEP}"
                status += (f"\nDeparture time: | "
                           f"{package.departure_time.isoformat(sep=" ", timespec="minutes")}"
                           f"\n{BaseCommand.TABLE_SEP}"
                           f"\nArrival time:   | "
                           f"{package.estimated_arrival_time.isoformat(sep=" ", timespec="minutes")}"
                           f"\n{BaseCommand.TABLE_SEP}")
            else:
                status = f"\nPackage status: | Not assigned\n{BaseCommand.TABLE_SEP}"
            return status

        result += ("\n".join([f"\nPACKAGE ID:     | {package.id}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nStart location: | {package.start_location}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nEnd location:   | {package.end_location}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nWeight:         | {package.weight:.2f} kg"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"\nCustomer email: | {package.customer_email}"
                            f"\n{BaseCommand.TABLE_SEP}"
                            f"{status_string(package)}" + BaseCommand.ROW_SEP for package in packages])
                   )

        self.logger.info(result)
        return result

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1

