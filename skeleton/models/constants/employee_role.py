class EmployeeRole:
    REGULAR = 'Regular'
    SUPERVISOR = 'Supervisor'
    MANAGER = 'Manager'

    @classmethod
    def from_string(cls, value) -> str:
        if value not in [cls.REGULAR, cls.SUPERVISOR, cls.MANAGER]:
            raise ValueError(
                f'None of the possible Employee Role values matches the value {value}.')

        return value
