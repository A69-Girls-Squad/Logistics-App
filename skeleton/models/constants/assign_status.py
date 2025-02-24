class AssignStatus:
    """
    Represents the possible assignment statuses for packages or tasks within the system.

    Attributes:
        ASSIGNED (str): Represents the status of an assigned package or task.
        UNASSIGNED (str): Represents the status of an unassigned package or task.
        ALL (str): Represents all statuses, including both assigned and unassigned.
    """
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    ALL = "all"

    @classmethod
    def from_string(cls, value: str) -> str:
        """
        Converts a string value into a valid assignment status.

        Args:
            value (str): The string value to convert into an assignment status.

        Returns:
            str: The validated assignment status.

        Raises:
            ValueError: If the provided value does not match any of the valid assignment statuses.
        """
        if value not in [cls.ASSIGNED, cls.UNASSIGNED, cls.ALL]:
            raise ValueError(
                f"None of the possible Status values matches the value {value}.")

        return value
