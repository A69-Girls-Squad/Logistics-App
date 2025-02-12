import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.package import Package
class SendPackageInfoToCustomerCommand:
    def __init__(self, package: Package):
        self.package = package

    def package_info(self):
        package_info = (
            f'Package ID: {self.package._id}\n'
            f'Start Location{self.package.start_location}\n'
            f'End Location{self.package.end_location}\n'
            f'Departure Time{self.package.departure_time}\n'
            f'Estimated Arrival Time{self.package.estimated_arrival_time}\n'
        )

        return package_info
    
    def send_email(self, subject, body, to_email):
        sender_email = "employee_email"
        sender_password = "employee_password" # can be skipped if the employee is already logged in?  
        smtp_server = "smtp.example.com"  
        smtp_port = 587  

        # Create the MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email using smtplib
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
                print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def execute(self):
        customer_email = self.package.customer_email
        package_details = self.package_info()
        subject = f"Package Details: {self.package._id}"

        self.send_email(subject, package_details, customer_email)