import smtplib
import logging

from commands.base_command import BaseCommand
from models.package import Package
from core.application_data import ApplicationData


"""
Sends info regarding a package to the customer.
"""
class SendPackageInfoToCustomerCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        self.logger = logging.getLogger(self.__class__.__name__)

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(message)s",
            datefmt="%d:%m:%Y %H:%M",
            level=logging.INFO
        )

    def package_info(self):
        package = self._params[0]
        package_info = (
            f"Package ID: {package.id}\n"
            f"Start Location: {package.start_location}\n"
            f"End Location: {package.end_location}\n"
            f"Departure Time: {package.departure_time}\n"
            f"Estimated Arrival Time: {package.estimated_arrival_time}\n"
        )
        return package_info
    

    def send_email(self, subject: str, body: str, customer_email: str):
        """
        Sends an email with the package information.

        """
        employee = self.app_data.logged_in_employee
        sender_email = employee.email
        sender_password = employee.password  # to do - take info from app data

        smtp_server = "smtp.logistics.com"
        smtp_port = 587

        message = f"Subject: {subject}\n\n{body}"
        message = f"Subject:{subject}\n\n{body}"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, customer_email, message)

        self.logger.info(f"Email successfully sent to {customer_email}")

    def execute(self):
        package = self._params[0]
        customer_email = package.customer_email
        package_details = self.package_info()
        subject = f"Package Details: {package.id}"

        self.logger.info(f"Package info sent to customer: {customer_email}")
        
        self.send_email(subject, package_details, customer_email)