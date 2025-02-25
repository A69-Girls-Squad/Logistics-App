import unittest

from models.constants.employee_role import EmployeeRole
from models.employee import Employee


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.valid_employee = Employee(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            password="Pass@123",
            employee_role=EmployeeRole.MANAGER
        )

    def test_valid_employee_creation(self):
        self.assertEqual(self.valid_employee.username, "john_doe")
        self.assertEqual(self.valid_employee.password, "Pass@123")
        self.assertEqual(self.valid_employee.employee_role, EmployeeRole.MANAGER)

    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            Employee(username="ab",
                     first_name="John",
                     last_name="Doe",
                     password="Pass@123",
                     employee_role=EmployeeRole.MANAGER)

        with self.assertRaises(ValueError):
            Employee(username="invalid_username_1234567890",
                     first_name="John",
                     last_name="Doe",
                     password="Pass@123",
                     employee_role=EmployeeRole.MANAGER)

    def test_invalid_first_name(self):
        with self.assertRaises(ValueError):
            Employee(username="john_doe",
                     first_name="J",
                     last_name="Doe",
                     password="Pass@123",
                     employee_role=EmployeeRole.MANAGER)

    def test_invalid_last_name(self):
        with self.assertRaises(ValueError):
            Employee(username="john_doe",
                     first_name="John",
                     last_name="D",
                     password="Pass@123",
                     employee_role=EmployeeRole.MANAGER)

    def test_invalid_password(self):
        with self.assertRaises(ValueError):
            Employee(username="john_doe",
                     first_name="John",
                     last_name="Doe",
                     password="short",
                     employee_role=EmployeeRole.MANAGER)
        with self.assertRaises(ValueError):
            Employee(username="john_doe",
                     first_name="John",
                     last_name="Doe",
                     password="a" * 29,
                     employee_role=EmployeeRole.MANAGER)
        with self.assertRaises(ValueError):
            Employee(username="john_doe",
                     first_name="John",
                     last_name="Doe",
                     password="Invalid!Password",
                     employee_role=EmployeeRole.MANAGER)

    def test_to_json(self):
        expected_json = {
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "password": "Pass@123",
            "employee_role": EmployeeRole.MANAGER
        }
        self.assertEqual(self.valid_employee.to_json(), expected_json)

    def test_from_json(self):
        data = {
            "username": "jane_doe",
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "StrongPass@1",
            "employee_role": EmployeeRole.MANAGER
        }
        employee = Employee.from_json(data)

        self.assertEqual(employee.__dict__["_username"], "jane_doe")
        self.assertEqual(employee.__dict__["_first_name"], "Jane")
        self.assertEqual(employee.__dict__["_last_name"], "Doe")
        self.assertEqual(employee.password, "StrongPass@1")
        self.assertEqual(employee.employee_role, EmployeeRole.MANAGER)
