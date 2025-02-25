import unittest
from commands.create_package import CreatePackageCommand
from errors.application_error import ApplicationError


class ApplicationData:
    def __init__(self):
        self.has_logged_in_employee = True
        self.logged_in_employee = "test_user"
        self.packages = []
        self.next_package_id = 1

    def create_package(self, start_location, end_location, weight, customer_email):
        package = {
            "id": self.next_package_id,
            "start_location": start_location,
            "end_location": end_location,
            "weight": weight,
            "customer_email": customer_email,
        }
        self.packages.append(package)
        self.next_package_id += 1
        return package

class CreatePackageCommandTests(unittest.TestCase):
    def setUp(self):
        self.app_data = ApplicationData()
        self.params = ["SYD", "MEL", "45.5", "customer@example.com"]

    def test_init_withValidArguments_createsInstance(self):
        # Act
        command = CreatePackageCommand(self.params, self.app_data)

        # Assert
        self.assertEqual(command.params, tuple(self.params))
        self.assertEqual(command.app_data, self.app_data)

    def test_execute_withValidParameters_createsPackageAndReturnsMessage(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.app_data)

        # Act
        result = command.execute()

        # Assert
        self.assertIn("Package with ID 1 was created!", result)
        self.assertIn("Start Location: | SYD", result)
        self.assertIn("End Location:   | MEL", result)
        self.assertIn("Weight:         | 45.5 kg", result)
        self.assertIn("Customer email: | customer@example.com", result)
        self.assertEqual(len(self.app_data.packages), 1)
        self.assertEqual(self.app_data.packages[0]["id"], 1)
        self.assertEqual(self.app_data.packages[0]["start_location"], "SYD")
        self.assertEqual(self.app_data.packages[0]["end_location"], "MEL")
        self.assertEqual(self.app_data.packages[0]["weight"], 45.5)
        self.assertEqual(self.app_data.packages[0]["customer_email"], "customer@example.com")

    def test_execute_withInvalidWeight_raisesApplicationError(self):
        # Arrange
        invalid_weight = "invalid"
        invalid_params = ["SYD", "MEL", invalid_weight, "customer@example.com"]
        command = CreatePackageCommand(invalid_params, self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid value. Should be a number.", str(context.exception))

    def test_execute_withInsufficientParameters_raisesApplicationError(self):
        # Arrange
        insufficient_params = ["SYD", "MEL", "45.5"]
        command = CreatePackageCommand(insufficient_params, self.app_data)

        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            command.execute()
        self.assertIn("Invalid number of arguments", str(context.exception))

    def test_requires_login_returnsTrue(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.app_data)

        # Act
        requires_login = command._requires_login()

        # Assert
        self.assertTrue(requires_login)

    def test_expected_params_count_returnsFour(self):
        # Arrange
        command = CreatePackageCommand(self.params, self.app_data)

        # Act
        expected_params = command._expected_params_count()

        # Assert
        self.assertEqual(expected_params, 4)

