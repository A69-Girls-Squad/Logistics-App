from commands.validation_helpers import validate_params_count, try_parse_float
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class CreatePackageCommand(BaseCommand):
    """
    Command to create a new package in the application.

    This command validates the input parameters, creates a package, and logs the action.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (start location, end location, weight, and customer email).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 4)
        super().__init__(params, app_data)


    def execute(self) -> str:
        """
        Executes the command to create a new package.

        Returns:
            str: A confirmation message indicating the package was created.

        Raises:
            ValueError: If any of the parameters are invalid (e.g., invalid weight or email format).
        """

        start_location, end_location, weight_float, customer_email = self._params
        weight = try_parse_float(weight_float)

        package = self.app_data.create_package(start_location, end_location, weight, customer_email)


        self.logger.info(f"Package with ID {package.id} created | Executed by: {self.app_data.logged_in_employee}")
        # return f"Package with ID {package.id} was created!"
        # self.logger.info(f"Package with ID {package.id} created" + self.ROW_SEP_SHORT)
        return f"Package with ID {package.id} was created!" + self.ROW_SEP
        self.logger.info(f"Package with ID {package.id} created | Executed by: {self.app_data.logged_in_employee}"+ self.ROW_SEP)

        return (f"Package with ID {package.id} was created!"
                f"\n{self.TABLE_SEP}"
                f"\nStart Location: | {start_location}"
                f"\n{self.TABLE_SEP}"
                f"\nEnd Location:   | {end_location}"
                f"\n{self.TABLE_SEP}"
                f"\nWeight:         | {weight_float} kg"
                f"\n{self.TABLE_SEP}"
                f"\nCustomer email: | {customer_email}"
                f"\n{self.TABLE_SEP}") + self.ROW_SEP*2
