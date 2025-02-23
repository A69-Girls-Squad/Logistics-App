class AssignStatus:
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    ALL = "all"

    @classmethod
    def from_string(cls, value) -> str:
        if value not in [cls.ASSIGNED, cls.UNASSIGNED, cls.ALL]:
            raise ValueError(
                f'None of the possible Status values matches the value {value}.')

        return value