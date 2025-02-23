class EmployeeRole:
    """
    Represents the possible roles an employee can have within the system.

    Attributes:
        REGULAR (str): Represents a regular employee role.
        SUPERVISOR (str): Represents a supervisor role.
        MANAGER (str): Represents a manager role.
    """
    REGULAR = 'Regular'
    SUPERVISOR = 'Supervisor'
    MANAGER = 'Manager'

    @classmethod
    def from_string(cls, value) -> str:
        """
        Converts a string value into a valid employee role.

        Args:
            value (str): The string value to convert into an employee role.

        Returns:
            str: The validated employee role.

        Raises:
            ValueError: If the provided value does not match any of the valid employee roles.
        """
        if value not in [cls.REGULAR, cls.SUPERVISOR, cls.MANAGER]:
            raise ValueError(
                f'None of the possible Employee Role values matches the value {value}.')
        return value