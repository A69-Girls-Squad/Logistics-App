import smtplib
from errors.application_error import ApplicationError
from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


"""
Sends info regarding a package to the customer.
"""
class SendPackageInfoToCustomerCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def package_info(self):
        package_id = try_parse_int(self._params[0])
        package = self.app_data.find_package_by_id(package_id)

        if not package:
            self.logger.error(f"Package with ID {package_id} not found.")
            raise ApplicationError(f"No package found with ID {package_id}")
        
        package_info = (
            f"Package ID: {package.id}\n"
            f"Start Location: {package.start_location}\n"
            f"End Location: {package.end_location}\n"
            f"Departure Time: {package.departure_time.isoformat(sep=" ", timespec="minutes")}\n"
            f"Estimated Arrival Time: {package.estimated_arrival_time.isoformat(sep=" ", timespec="minutes")}\n"
        )
        return package_info
    
    def send_email(self, subject: str, body: str, customer_email: str):
        """
        Sends an email with the package information.

        """
        employee = self.app_data.logged_in_employee
        sender_email = employee.smtp.email
        sender_password = employee.smtp.password 

        smtp_server = "smtp.logistics.com"
        smtp_port = 587

        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, customer_email, message)

        self.logger.info(f"Email successfully sent to {customer_email}")

    def execute(self):
        package_id = try_parse_int(self._params[0])
        package = self.app_data.find_package_by_id(package_id)
        customer_email = package.customer_email
        package_details = self.package_info()
        subject = f"Package Details: {package.id}"

        self.logger.info(f"Package info sent to customer: {customer_email}" + self.ROW_SEP)
        
        self.send_email(subject, package_details, customer_email)