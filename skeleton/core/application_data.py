from datetime import datetime
from errors.application_error import ApplicationError
from models.employee import Employee
from models.truck import Truck
from models.package import Package
from models.route import Route


class ApplicationData:
    def __init__(self):
        self._trucks = []
        self._routes = []
        self._packages = []
        self._employees = []
        self._logged_in_employee = None

    @classmethod
    def from_json(cls, data):
        """
        Converts a JSON into ApplicationData.
        """
        app_data = cls()
        app_data._packages = [Package.from_json(package_data) for package_data in data["packages"]]
        app_data._employees = [Employee.from_json(employees_data) for employees_data in data["employees"]]
        app_data._trucks = [Truck.from_json(trucks_data) for trucks_data in data["trucks"]]
        app_data._routes = [Route.from_json(routes_data) for routes_data in data["routes"]]

        return app_data

    def to_json(self):
        """
        Converts the ApplicationData class into a JSON.
        """
        return {
            "trucks": [truck.to_json() for truck in self._trucks],
            "routes": [route.to_json() for route in self._routes],
            "packages": [package.to_json() for package in self._packages],
            "employees": [employee.to_json() for employee in self._employees]}

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
        self._logged_in_employee = value

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

    def create_truck(self, name: str, capacity: int, max_range: int):
        truck = Truck(name, capacity, max_range)
        self._trucks.append(truck)

    def create_route(self, locations: str, departure_time: str):
        """
        Creates a new route and adds it to the application"s routes list.
        Data validation is handled by the Route class __init__ constructor.
        """
        route = Route(locations, departure_time)
        self._routes.append(route)

        return route

    def create_package(self, start_location: str, end_location: str, weight: float, customer_email: str) -> Package:
        """
        Creates a new package and adds it to the application"s packages list.
        Data validation is handled by the Package class __init__ constructor.
        """
        package = Package(start_location, end_location, weight, customer_email)
        self._packages.append(package)

        return package

    def create_employee(self, username, first_name, last_name, password, employee_role) -> Employee:
        """
        Creates a new employee and adds them to the employee list.
        Returns the newly created employee object.
        Checks if an employee with the given `username` already exists.
        """
        if len([employee for employee in self._employees if employee.username == username]) > 0:
            raise ApplicationError(f"Employee {username} already exist. Choose a different username!")

        employee = Employee(username, first_name, last_name, password, employee_role)
        self._employees.append(employee)

        return employee

    def assign_truck_to_route(self, truck_id: int, route_id: int):
        truck = self.find_truck_by_id(truck_id)
        if truck is None:
            raise ApplicationError(f"Truck with ID {truck_id} does not exist")

        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")

        if truck.assigned_route_id:
            raise ApplicationError(f"Truck with ID {truck_id} is already assigned")
        if route.assigned_truck_id:
            raise ApplicationError(f"Route with ID {route_id} already has a Truck assigned")

        if route.load > truck.capacity:
            raise ApplicationError("Not enough capacity.")
        if route.distance > truck.max_range:
            raise ApplicationError("Truck max range exceeded.")

        truck.assigned_route_id = route.id
        route.assigned_truck_id = truck.id
        route.assigned_truck_capacity = truck.capacity

    def unassign_truck_from_route(self, truck_id):
        truck = self.find_truck_by_id(truck_id)
        route = self.find_route_by_id(truck.assigned_route_id)
        truck.assigned_route_id = None
        route.assigned_truck_id = None
        route.assigned_truck_capacity = None

    def assign_package_to_route(self, package_id: int, route_id: int):
        package = self.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")
        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")

        if package.is_assigned:
            raise ApplicationError(f"Package with ID {package_id} is already assigned")
        if package.route_id == route_id or package_id in route.assigned_packages_ids:
            raise ApplicationError(f"Package with ID {package_id} is already assigned to Route with ID {route_id}")

        # redundant
        # if not route.assigned_truck_id:
        #     raise ApplicationError(f"No Truck is assigned to Route with ID {route_id}")
        if route.assigned_truck_id:
            truck = self.find_truck_by_id(route.assigned_truck_id)
            free_capacity = truck.capacity - route.load
            if free_capacity < package.weight:
                raise ApplicationError(f"Route with ID {route_id} has no more capacity")
        if route.departure_time < datetime.now():
            raise ApplicationError(f"Assigned Truck to Route with ID {route_id} has already departed")
        if package.start_location not in route.locations:
            raise ApplicationError(f"Package with ID {package_id} start location "
                                   f"does not exists in Route with ID {route_id}")

        package.departure_time = route.departure_time
        package.estimated_arrival_time = route.stops[package.end_location]
        package.route_id = route.id
        route.assign_package(package.id)
        route.load += package.weight

    def unassign_package_from_route(self, package_id: int, route_id: int):
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
        route.remove_package(package.id)
        route.load -= package.weight

    def get_packages_by_assigned_status(self, is_assigned: bool) -> list:
        """
        Returns a list of packages based on their assigned status.

        Args:
            is_assigned (bool): The status to filter packages by.
                                If True, returns packages that are assigned.
                                If False, returns packages that are not assigned.

        Returns:
            list: A list of packages that match the specified assigned status.
        """
        return [package for package in self._packages if package.is_assigned == is_assigned]

    def find_truck_by_id(self, truck_id: int) -> Truck:
        """
        Finds and returns the truck associated with the provided ID.
        If no match is found, returns `None`.
        """
        return next((truck for truck in self.trucks if truck.id == truck_id), None)

    def find_route_by_id(self, route_id: int) -> Route:
        """
        Finds and returns the route associated with the provided ID.
        If no match is found, returns `None`.
        """
        return next((route for route in self.routes if route.id == route_id), None)

    def find_package_by_id(self, package_id: int) -> Package:
        """
        Finds and returns the package associated with the provided ID.
        If no match is found, returns `None`.
        """
        for package in self.packages:
            if package.id == package_id:
                return package

    def find_employee_by_username(self, username: str) -> Employee:
        """
        Finds and returns the employee associated with the provided username.
        If no match is found, returns `None`.
        """
        return next((employee for employee in self.employees if employee.username == username), None)

    def login(self, employee: Employee):
        """
        Logs in an employee by setting the provided employee as the currently logged-in user.
        """
        self._logged_in_employee = employee

    def logout(self):
        """
        Logs out the currently logged-in employee by setting the logged-in employee to `None`.
        After calling this method, no employee will be considered logged in until a new `login` method is called.
        """
        self._logged_in_employee = None