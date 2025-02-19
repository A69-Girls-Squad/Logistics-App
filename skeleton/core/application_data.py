from datetime import datetime
from skeleton.errors.application_error import ApplicationError
from skeleton.models.employee import Employee
from skeleton.models.truck import Truck
from skeleton.models.package import Package
from skeleton.models.route import Route


class ApplicationData:

    @classmethod
    def from_json(cls, data):
        """
        Converts a JSON into ApplicationData.
        """
        app_data = cls()

        app_data._packages = [Package.from_json(package_data) for package_data in
                              data["_packages"]]

        return app_data

    def __init__(self):
        self._trucks = []
        self._routes = []
        self._packages = []
        self._employees = []
        self._logged_in_employee = None

    """
    Returns the entire truck park as an immutable tuple of truck objects.
    """
    @property
    def trucks(self):
        return tuple(self._trucks)

    """
    Returns all created routes.
    """
    @property
    def routes(self):
        return tuple(self._routes)

    """
    Returns all created packages.
    """
    @property
    def packages(self):
        return tuple(self._packages)

    """
    Returns all created employees.
    """
    @property
    def employees(self):
        return tuple(self._employees)

    """
    Manages the currently logged-in employee.

    Retrieves or updates the employee who is currently logged in.
    Ensures only valid `Employee` objects can be assigned.
    """
    @property
    def logged_in_employee(self):
        return self._logged_in_employee

    @logged_in_employee.setter
    def logged_in_employee(self, value: Employee):
        try:
            if not isinstance(value, Employee):
                raise ApplicationError("Invalid employee")
            self._logged_in_employee = value
        except ApplicationError as ae:
            print(ae.args[0])

    """
    Indicates whether an employee is currently logged in.
    
    Checks if there is a logged-in employee.
    Returns `True` if an employee is logged in, otherwise `False`.
    """
    @property
    def has_logged_in_employee(self):
        return self.logged_in_employee is not None

    """
    Retrieves a list of all packages that are not assigned to a route.
    """
    @property
    def not_assigned_packages(self):
        not_assigned_packages = []
        for package in self.packages:
            if not package.is_assigned:
                not_assigned_packages.append(package)
        return not_assigned_packages

    def create_package(self, start_location: str, end_location: str, weight: float, customer_email: str) -> Package:
        """
        Creates a new package and adds it to the application"s packages list.
        Data validation is handled by the Package class __init__ constructor.
        """
        package = Package(start_location, end_location, weight, customer_email)
        self._packages.append(package)

        return package

    def create_route(self, locations: str, departure_time: str):
        """
        Creates a new route and adds it to the application"s routes list.
        Data validation is handled by the Route class __init__ constructor.
        """
        route = Route(locations, departure_time)
        self._routes.append(route)

        return route

    def create_truck(self, name: str, capacity: int, max_range: int):
        truck = Truck(name, capacity, max_range)
        self._trucks.append(truck)

    def find_package_by_id(self, id: int) -> Package:
        """
        Finds and returns the package associated with the provided ID.
        If no match is found, returns `None`.
        """
        for package in self.packages:
            if package.id == id:
                return package

    def find_route_by_id(self, id) -> Route:
        """
        Finds and returns the route associated with the provided ID.
        If no match is found, returns `None`.
        """
        for route in self.routes:
            if route.id == id:
                return route

    def find_truck_by_id(self, id) -> Truck:
        """
        Finds and returns the truck associated with the provided ID.
        If no match is found, returns `None`.
        """
        for truck in self.trucks:
            if truck.id == id:
                return truck

    def create_employee(self, username, firstname, lastname, password, employee_role) -> Employee:
        """
        Creates a new employee and adds them to the employee list.
        Returns the newly created employee object.
        Checks if an employee with the given `username` already exists.
        """
        try:
            if len([u for u in self._employees if u.username == username]) > 0:
                raise ValueError(f"Employee {username} already exist. Choose a different username!")

            employee = Employee(username, firstname, lastname, password, employee_role)
            self._employees.append(employee)

            return employee

        except ApplicationError as ae:
            print(ae.args[0])

    def find_employee_by_username(self, username: str) -> Employee:
        """
        Finds and returns the employee associated with the provided username.
        If no match is found, returns `None`.
        """
        try:
            filtered = [employee for employee in self._employees if employee.username == username]
            if not filtered:
                raise ApplicationError(f"There is no employee with username {username}!")

            return filtered[0]

        except ApplicationError as ae:
            print(ae.args[0])

    def login(self, employee: Employee):
        """
        Logs in an employee by setting the provided employee as the currently logged-in user.
        """
        try:
            if not isinstance(employee, Employee):
                raise ApplicationError("Invalid employee")
            self._logged_in_employee = employee

        except ApplicationError as ae:
            print(ae.args[0])

    def logout(self):
        """
        Logs out the currently logged-in employee by setting the logged-in employee to `None`.
        After calling this method, no employee will be considered logged in until a new `login` method is called.
        """
        self._logged_in_employee = None

    def get_packages_by_assigned_status(self, is_assigned: bool) -> list:
        """
        Retrieves a list of packages that match the specified assignment status.

        Parameters:
        `is_assigned` (bool): The assignment status to filter by.
          - `True` returns packages that are assigned.
          - `False` returns packages that are not assigned.
        """
        result = []
        for package in self._packages:
            if package.is_assigned == is_assigned:
                result.append(package)

        return result

    def assign_package_to_route(self, package_id: int, route_id: str):
        package = self.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")
        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")

        if package.is_assigned:
            raise ApplicationError(f"Package with ID {package_id} is already assigned")
        if package.route_id == route_id or package_id in route.assigned_package_ids:
            raise ApplicationError(f"Package with ID {package_id} is already assigned to Route with ID {route_id}")

        if route.assigned_truck:
            raise ApplicationError(f"No Truck is assigned to Route with ID {route_id}")
        if route.free_capacity < package.weight:
            raise ApplicationError(f"Route with ID {route_id} has no more capacity")
        if route.departure_time > datetime.now():
            raise ApplicationError(f"Assigned Truck to Route with ID {route_id} has already departed")
        if package.start_location not in route.locations:
            raise ApplicationError(f"Package with ID {package_id} start location does not exists in Route with ID {route_id}")
        # end location check error

        package.departure_time = route.departure_time
        package.estimated_arrival_time = route.stops[package.end_location]
        package.route_id = route.id
        package.is_assigned = True
        route.assigned_package_ids.append(package.id)
        route.load += package.weight

    def unassign_package_from_route(self, package_id: int, route_id: str):
        package = self.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")

        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")
        if route.departure_time > datetime.now():
            raise ApplicationError(f"Assigned Truck to Route with ID {route_id} has already departed")

        package.departure_time = None
        package.estimated_arrival_time = None
        package.route_id = None
        package.is_assigned = False
        route.assigned_package_ids.remove(package.id)
        route.load -= package.weight

    def to_json(self):
        """
        Converts the ApplicationData class into a JSON.
        """
        return {
            #"_trucks": [truck.to_json() for truck in self._trucks],
            #"_routes": [route.to_json() for route in self._routes],
            "_packages": [package.to_json() for package in self._packages]}
            #"_employees": [employee.to_json() for employee in self._employees]}

