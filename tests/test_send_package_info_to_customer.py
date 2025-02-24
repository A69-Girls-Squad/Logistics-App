import unittest
from unittest.mock import MagicMock
from skeleton.commands.send_package_info_to_customer import SendPackageInfoToCustomerCommand
from skeleton.core.application_data import ApplicationData
from skeleton.errors.application_error import ApplicationError

class TestSendPackageInfoToCustomerCommand(unittest.TestCase):

    def test_package_info_found(self):
        params = ["101"]
        app_data_mock = MagicMock(ApplicationData)
        package_mock = MagicMock()
        package_mock.id = 101
        package_mock.start_location = "Start Location"
        package_mock.end_location = "End Location"
        package_mock.departure_time.isoformat.return_value = "2025-02-27 10:00"
        package_mock.estimated_arrival_time.isoformat.return_value = "2025-02-28 16:00"
        package_mock.customer_email = "customer@test.com"

        app_data_mock.find_package_by_id.return_value = package_mock

        cmd = SendPackageInfoToCustomerCommand(params, app_data_mock)
        
        cmd.send_email = MagicMock()

        cmd.execute()

        expected_email_body = (
            "Package ID: 101\n"
            "Start Location: Start Location\n"
            "End Location: End Location\n"
            "Departure Time: 2025-02-27 10:00\n"
            "Estimated Arrival Time: 2025-02-28 16:00\n"
        )

        cmd.send_email.assert_called_once_with(
            "Package Details: 101",
            expected_email_body,
            "customer@test.com"
        )

    def test_package_not_found(self):
        params = ["101"]
        app_data_mock = MagicMock(ApplicationData)

        app_data_mock.find_package_by_id.return_value = None

        cmd = SendPackageInfoToCustomerCommand(params, app_data_mock)

        with self.assertRaises(ApplicationError):
            cmd.execute()

    def test_send_email_called(self):
        params = ["101"]
        app_data_mock = MagicMock(ApplicationData)
        package_mock = MagicMock()
        package_mock.id = 101
        package_mock.customer_email = "customer@test.com"
        package_mock.start_location = "Start Location"
        package_mock.end_location = "End Location"
        package_mock.departure_time.isoformat.return_value = "2025-02-27 10:00"
        package_mock.estimated_arrival_time.isoformat.return_value = "2025-02-28 16:00"

        app_data_mock.find_package_by_id.return_value = package_mock

        cmd = SendPackageInfoToCustomerCommand(params, app_data_mock)
        cmd.send_email = MagicMock()

        cmd.execute()

        expected_email_body = (
            "Package ID: 101\n"
            "Start Location: Start Location\n"
            "End Location: End Location\n"
            "Departure Time: 2025-02-27 10:00\n"
            "Estimated Arrival Time: 2025-02-28 16:00\n"
        )

        cmd.send_email.assert_called_once_with(
            "Package Details: 101",
            expected_email_body,
            "customer@test.com"
        )