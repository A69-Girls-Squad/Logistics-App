import re
from skeleton.commands.validation_helpers import try_parse_float


class Package:

    # STATUS_NOT_ASSIGNED = "Not assigned"
    # STATUS_ASSIGNED = "Assigned"  ..... - 15/02 >=< datetime.datetime.now()
    # on delivery   16/02 - 18/02
    # delivered     19/02 - .....  >=< datetime.datetime.now()

    _current_id = 0

    _email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+") #convert a regex pattern into a regex object

    @classmethod
    def next_id(cls):
        cls._current_id += 1
        return cls._current_id

    def __init__(self, start_location: str, end_location: str, weight: float, customer_email: str):
        self._id = Package.next_id()
        self._start_location = start_location #  for validation
        self._end_location = end_location#  for validation; setter
        if weight < 0:
            raise ValueError("Weight can not be negative number")
        self._weight = try_parse_float(weight)
        if not Package._email_regex.fullmatch(customer_email):
            raise ValueError(f"Invalid email address: {customer_email}")
        self._customer_email = customer_email
        self._departure_time = None
        self._estimated_arrival_time = None   # use route.stops.value for the end location
        self._is_assigned = False   # if self._route: True, else: False
        self._route = None #?
        # self.status

    @property
    def id(self):
        return self._id

    @property
    def start_location(self):
        return self._start_location

    @property
    def end_location(self):
        return self._end_location

    @property
    def weight(self):
        return self._weight

    @property
    def customer_email(self):
        return self._customer_email

    @property
    def departure_time(self):
        return self._departure_time

    @property
    def estimated_arrival_time(self):
        return self._estimated_arrival_time

    @property
    def is_assigned(self):
        return self._is_assigned

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, value):
        self._route = value

    def __str__(self):
        return (f"ID: {self._id}"
                f"\nStart Location: {self._start_location})"
                f"\nEnd Location: {self._end_location}"
                f"\nWeight: {self._weight:.2f}kg"
                f"\nCustomer Email Address: {self._customer_email}"
                f"\nDeparture time: {self._departure_time}"
                f"\nEstimated arrival time: {self._estimated_arrival_time}")



