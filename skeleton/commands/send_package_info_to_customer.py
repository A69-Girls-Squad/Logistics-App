import smtplib
import logging
from skeleton.models.package import Package
from skeleton.core.application_data import ApplicationData
class SendPackageInfoToCustomerCommand:
    def __init__(self, package: Package, app_data: ApplicationData):
        self.package = package
        self.app_data = app_data
        self.logger = logging.getLogger(self.__class__.__name__)

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(message)s",
            datefmt="%d:%m:%Y %H:%M",
            level=logging.INFO
        )

    def package_info(self):
        package_info = (
            f'Package ID: {self.package._id}\n'
            f'Start Location: {self.package.start_location}\n'
            f'End Location: {self.package.end_location}\n'
            f'Departure Time: {self.package.departure_time}\n'
            f'Estimated Arrival Time: {self.package.estimated_arrival_time}\n'
        )
        return package_info
    
    def send_email(self, subject, body, customer_email):
        employee = self._app_data.logged_in_employee 
        sender_email = employee.email
        sender_password = employee.password # can be skipped if the employee is already logged in?  
        smtp_server = "smtp.logistics.com"  
        smtp_port = 587 

        message = f'Subject:{subject}\n\n{body}'

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, customer_email, message)
                print(f"Email sent to {customer_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def execute(self):
        customer_email = self.package.customer_email
        package_details = self.package_info()
        subject = f"Package Details: {self.package._id}"

        self.logger.info(f'Package info sent to customer: {customer_email}')
        
        self.send_email(subject, package_details, customer_email)