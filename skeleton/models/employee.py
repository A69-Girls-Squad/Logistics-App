import re
from models.constants.employee_role import EmployeeRole


class Employee:
    """
    Represents an employee with a username, first name, last name, password, and role.

    Attributes:
        _username (str): The unique username of the employee. Must be 3-20 characters long
                         and can contain letters, numbers, and underscores (but not start or end with one).
        _first_name (str): The first name of the employee. Must be 1-30 characters long and can contain
                          letters, spaces, and hyphens.
        _last_name (str): The last name of the employee. Must be 1-30 characters long and can contain
                         letters, spaces, and hyphens.
        _password (str): The password of the employee. Must be between 6 and 28 characters and can contain
                         letters, numbers, and special symbols (@, *, -, _).
        _employee_role (EmployeeRole): The role assigned to the employee.

    Methods:
        from_json(data: dict) -> Employee: Creates an Employee instance from a JSON-compatible dictionary.
        to_json() -> dict: Converts the Employee instance into a JSON-compatible dictionary.
        username() -> str: Returns the employee's username.
        password() -> str: Returns the employee's password.
        __str__() -> str: Returns a string representation of the employee.

    Raises:
        ValueError: If any attribute does not meet validation criteria.
    """

    def __init__(self, username: str, first_name: str, last_name: str, password: str, employee_role: EmployeeRole):
        """
        Initializes an Employee instance.

        Args:
            username (str): The unique username (3-20 characters, alphanumeric with optional underscores).
            first_name (str): The first name (1-30 characters, only letters, spaces, and hyphens allowed).
            last_name (str): The last name (1-30 characters, only letters, spaces, and hyphens allowed).
            password (str): The password (6-28 characters, letters, numbers, and special symbols @, *, -, _).
            employee_role (EmployeeRole): The role assigned to the employee.

        Raises:
            ValueError: If any of the attributes do not meet the specified validation rules.
        """
        if len(username) < 3 or len(username) > 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        if not re.match(r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$", username):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores (but not start or end with one).")
        self._username = username

        if len(first_name) > 30 or len(first_name) < 2:
            raise ValueError("Name must be between 2 and 30 characters.")
        if not first_name.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("First name can only contain letters, spaces, and hyphens.")
        self._first_name = first_name

        if len(last_name) > 30 or len(last_name) < 2:
            raise ValueError("Last name must be between 2 and 30 characters.")
        if not last_name.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("Last name can only contain letters, spaces, and hyphens.")
        self._last_name = last_name

        special_char = ["@", "*", "-", "_"]
        if len(password) > 28 or len(password) < 6:
            raise ValueError("Password must be between 6 and 28 characters long.")
        for char in password:
            if char not in special_char and not char.isalnum():
                raise ValueError("Invalid symbols! Password can only contains letters,"
                                 " numbers and special symbols @, *, -, _")
        self._password = password
        self._employee_role = employee_role


    @classmethod
    def from_json(cls, data: dict):
        """
        Creates an Employee instance from a JSON-compatible dictionary.

        Args:
            data (dict): A dictionary containing employee details, including:
                - username (str): The employee's username.
                - first_name (str): The employee's first name.
                - last_name (str): The employee's last name.
                - password (str): The employee's password.
                - employee_role (str): The employee's role as a string.

        Returns:
            Employee: An instance of the Employee class.
        """
        employee = cls(
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
            employee_role=EmployeeRole(data["employee_role"])
        )

        return employee

    def to_json(self) -> dict:
        """
        Converts the Employee instance into a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the employee, including:
                - username (str): The employee's username.
                - first_name (str): The employee's first name.
                - last_name (str): The employee's last name.
                - password (str): The employee's password.
                - employee_role (str): The employee's role as a string.
        """
        return {
            "username": self._username,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "password": self._password,
            "employee_role": self._employee_role
        }

    @property
    def username(self) -> str:
        """
        Gets the employee's username.

        Returns:
            str: The employee's username.
        """
        return self._username

    @property
    def password(self) -> str:
        """
        Gets the employee's password.

        Returns:
            str: The employee's password.
        """
        return self._password

    def __str__(self):
        """
        Returns a string representation of the employee.

        Returns:
            str: A formatted string containing the employee's details.
        """
        return (f"Employee:"
                f"\n Username: {self._username}"
                f"\n First name: {self._first_name}"
                f"\n Last name: {self._last_name}"
                f"\n Role: {self._employee_role}")

