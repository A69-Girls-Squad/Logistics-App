import re
from models.constants.employee_role import EmployeeRole


class Employee:
    """
    Represents an employee with a username, first name, last name, password, and role.

    Attributes:
        _username (str): The unique username of the employee. Must be 3-20 characters long
                         and can contain letters, numbers, and underscores (but not start or end with one).
        _firstname (str): The first name of the employee. Must be 1-30 characters long and can contain
                          letters, spaces, and hyphens.
        _lastname (str): The last name of the employee. Must be 1-30 characters long and can contain
                         letters, spaces, and hyphens.
        _password (str): The password of the employee. Must be between 12 and 64 characters.
        _employee_role (EmployeeRole): The role assigned to the employee.

    Methods:
        username() -> str: Returns the employee's username.
        firstname() -> str: Returns the employee's first name.
        lastname() -> str: Returns the employee's last name.
        password() -> str: Returns the employee's password.
        employee_role() -> EmployeeRole: Returns the employee's role.
        __str__() -> str: Returns a string representation of the employee.

    Raises:
        ValueError: If any attribute does not meet validation criteria.
    """

    def __init__(self, username: str, firstname: str, lastname: str, password: str, employee_role: EmployeeRole):
        """
        Initializes an Employee instance.

        Args:
            username (str): The unique username (3-20 characters, alphanumeric with optional underscores).
            firstname (str): The first name (1-30 characters, only letters, spaces, and hyphens allowed).
            lastname (str): The last name (1-30 characters, only letters, spaces, and hyphens allowed).
            password (str): The password (12-64 characters).
            employee_role (EmployeeRole): The role assigned to the employee.

        Raises:
            ValueError: If any of the attributes do not meet the specified validation rules.
                """
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
            raise ValueError("Password must be at least 12 characters and maximum 64 characters.")
        self._password = password
        self._employee_role = employee_role


    @classmethod
    def from_json(cls, data: dict):
        employee = cls(
            username=data["username"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            password=data["password"],
            employee_role=EmployeeRole(data["employee_role"])
        )

        return employee

    def to_json(self) ->dict:
        return {
            "username": self._username,
            "firstname": self._firstname,
            "lastname": self._lastname,
            "password": self._password,
            "employee_role": self._employee_role
        }

    @property
    def username(self):
        """Returns the employee's username."""
        return self._username

    @property
    def password(self):
        """Returns the employee's password."""
        return self._password

    def __str__(self):
        """Returns a string representation of the employee."""
        return (f"Employee:"
                f"\n username={self._username}"
                f"\n firstname={self._firstname}"
                f"\n lastname={self._lastname}"
                f"\n role={self._employee_role})")

