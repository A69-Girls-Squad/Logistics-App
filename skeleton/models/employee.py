import re
from skeleton.models.constants.employee_role import EmployeeRole


class Employee:
    def __init__(self, username: str, firstname: str, lastname: str, password: str, employee_role: EmployeeRole):
        if len(username) > 20 or len(username) < 3:
            raise ValueError("Username must be between 3 and 30 characters.")
        if not re.match(r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$", username):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores (but not start or end with one).")
        self._username = username

        if len(firstname) > 30 or len(firstname) < 1:
            raise ValueError("Name must be between 2 and 30 characters.")
        if not firstname.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("First name an only contain letters, spaces, and hyphens.")
        self._firstname = firstname

        if len(lastname) > 30 or len(lastname) < 1:
            raise ValueError("Last name must be between 2 and 30 characters.")
        if not lastname.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("Last name can only contain letters, spaces, and hyphens.")
        self._lastname = lastname

        if len(password) > 64 or len(password) < 12:
            raise ValueError("Password must be at least 12 characters.")
        self._password = password
        self._employee_role = employee_role


    @property
    def username(self):
        return self._username

    def firstname(self):
        return self._firstname

    def lastname(self):
        return self._lastname

    def password(self):
        return self._password

    def employee_role(self):
        return self._employee_role
