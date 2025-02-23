from core.application_time import ApplicationTime
from errors.application_error import ApplicationError
from models.constants.employee_role import EmployeeRole
from models.employee import Employee
from models.truck import Truck
from models.package import Package
from models.route import Route


class ApplicationData:
    """
    Central class for managing application data, including trucks, routes, packages, and employees.

    This class provides methods for creating, retrieving, and managing the application's core entities.
    It also handles operations like assigning trucks to routes, assigning packages to routes, and managing employee login/logout.

    Attributes:
        _trucks (list[Truck]): A list of all trucks in the application.
        _routes (list[Route]): A list of all routes in the application.
        _packages (list[Package]): A list of all packages in the application.
        _employees (list[Employee]): A list of all employees in the application.
        _logged_in_employee (Employee): The currently logged-in employee.
    """
    def __init__(self):
        """
        Initializes the ApplicationData with empty lists for trucks, routes, packages, and employees.
        """
        self._trucks: list[Truck] = []
        self._routes: list[Route] = []
        self._packages: list[Package] = []
        self._employees: list[Employee] = []
        self._logged_in_employee = None

    @classmethod
    def from_json(cls, data):
        """
        Converts a JSON-compatible dictionary into an ApplicationData instance.

        Args:
            data (dict): A dictionary containing data for trucks, routes, packages, and employees.

        Returns:
            ApplicationData: An instance of ApplicationData populated with the provided data.
        """
        app_data = cls()
        app_data._packages = [Package.from_json(package_data) for package_data in data["packages"]]
        app_data._employees = [Employee.from_json(employees_data) for employees_data in data["employees"]]
        app_data._trucks = [Truck.from_json(trucks_data) for trucks_data in data["trucks"]]
        app_data._routes = [Route.from_json(routes_data) for routes_data in data["routes"]]

        return app_data

    def to_json(self):
        """
        Converts the ApplicationData instance into a JSON-compatible dictionary.

        Returns:
            dict: A dictionary containing data for trucks, routes, packages, and employees.
        """
        return {
            "trucks": [truck.to_json() for truck in self._trucks],
            "routes": [route.to_json() for route in self._routes],
            "packages": [package.to_json() for package in self._packages],
            "employees": [employee.to_json() for employee in self._employees]}

    @property
    def trucks(self) -> tuple:
        """
        Gets all trucks in the application as an immutable tuple.

        Returns:
            tuple[Truck]: A tuple of all trucks.
        """
        return tuple(self._trucks)

    @property
    def routes(self) -> tuple:
        """
        Gets all routes in the application as an immutable tuple.

        Returns:
            tuple[Route]: A tuple of all routes.
        """
        return tuple(self._routes)

    @property
    def packages(self) -> tuple:
        """
        Gets all packages in the application as an immutable tuple.

        Returns:
            tuple[Package]: A tuple of all packages.
        """
        return tuple(self._packages)

    @property
    def employees(self) -> tuple:
        """
        Gets all employees in the application as an immutable tuple.

        Returns:
            tuple[Employee]: A tuple of all employees.
        """
        return tuple(self._employees)

    @property
    def logged_in_employee(self):
        """
        Gets the currently logged-in employee.

        Returns:
            Employee: The logged-in employee, or `None` if no employee is logged in.
        """
        return self._logged_in_employee

    @logged_in_employee.setter
    def logged_in_employee(self, value: Employee):
        """
        Sets the currently logged-in employee.

        Args:
            value (Employee): The employee to set as logged in.

        Raises:
            ValueError: If the provided value is not an instance of `Employee`.
        """
        self._logged_in_employee = value

    @property
    def has_logged_in_employee(self):
        """
        Checks if an employee is currently logged in.

        Returns:
            bool: `True` if an employee is logged in, otherwise `False`.
        """
        return self.logged_in_employee is not None

    def create_truck(self, name: str, capacity: int, max_range: int):
        """
        Creates a new truck and adds it to the application's truck list.

        Args:
            name (str): The name of the truck.
            capacity (int): The capacity of the truck in kilograms.
            max_range (int): The maximum range of the truck in kilometers.

        Returns:
            Truck: The newly created truck.
        """
        truck = Truck(name, capacity, max_range)
        self._trucks.append(truck)

    def create_route(self, locations: str, departure_time: str):
        """
        Creates a new route and adds it to the application's route list.

        Args:
            locations (str): A string of locations separated by commas.
            departure_time (str): The departure time in ISO format.

        Returns:
            Route: The newly created route.
        """
        route = Route(locations, departure_time)
        self._routes.append(route)

        return route

    def create_package(self, start_location: str, end_location: str, weight: float, customer_email: str) -> Package:
        """
        Creates a new package and adds it to the application's package list.

        Args:
            start_location (str): The starting location of the package.
            end_location (str): The destination location of the package.
            weight (float): The weight of the package in kilograms.
            customer_email (str): The email address of the customer.

        Returns:
            Package: The newly created package.
        """
        package = Package(start_location, end_location, weight, customer_email)
        self._packages.append(package)

        return package

    def create_employee(self, username: str, first_name: str, last_name: str, password: str, employee_role: EmployeeRole) -> Employee:
        """
        Creates a new employee and adds them to the application's employee list.

        Args:
            username (str): The username of the employee.
            first_name (str): The first name of the employee.
            last_name (str): The last name of the employee.
            password (str): The password of the employee.
            employee_role (str): The role of the employee.

        Returns:
            Employee: The newly created employee.

        Raises:
            ApplicationError: If an employee with the same username already exists.
        """
        if len([employee for employee in self._employees if employee.username == username]) > 0:
            raise ApplicationError(f"Employee {username} already exist. Choose a different username!")
        employee = Employee(username, first_name, last_name, password, employee_role)
        self._employees.append(employee)

        return employee

    def assign_truck_to_route(self, truck_id: int, route_id: int):
        """
        Assigns a truck to a route.

        Args:
            truck_id (int): The ID of the truck to assign.
            route_id (int): The ID of the route to assign the truck to.

        Raises:
            ApplicationError: If the truck or route does not exist, or if the truck or route is already assigned.
        """
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
        """
        Unassigns a truck from its assigned route.

        Args:
            truck_id (int): The ID of the truck to unassign.

        Raises:
            ApplicationError: If the truck does not exist or is not assigned to a route.
        """
        truck = self.find_truck_by_id(truck_id)
        route = self.find_route_by_id(truck.assigned_route_id)
        truck.assigned_route_id = None
        route.assigned_truck_id = None
        route.assigned_truck_capacity = None

    def assign_package_to_route(self, package_id: int, route_id: int):
        """
        Assigns a package to a route.

        Args:
            package_id (int): The ID of the package to assign.
            route_id (int): The ID of the route to assign the package to.

        Raises:
            ApplicationError: If the package or route does not exist, or if the package is already assigned.
        """
        package = self.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")
        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")

        if package.route_id == route_id or package_id in route.assigned_packages_ids:
            raise ApplicationError(f"Package with ID {package_id} is already assigned to Route with ID {route_id}")
        if package.is_assigned:
            raise ApplicationError(f"Package with ID {package_id} is already assigned")

        # When no truck is assigned to route, package assignment is impossible
        if not route.assigned_truck_id:
             raise ApplicationError(f"No Truck is assigned to Route with ID {route_id}")

        truck = self.find_truck_by_id(route.assigned_truck_id)
        if truck is None:
            raise ApplicationError(f"Truck with ID {route.assigned_truck_id} does not exist")

        free_capacity = truck.capacity - route.load
        if free_capacity < package.weight:
            raise ApplicationError(f"Route with ID {route_id} has no more capacity")
        if route.departure_time < ApplicationTime.current():
            raise ApplicationError(f"Assigned Truck to Route with ID {route_id} has already departed")
        if package.start_location not in route.locations:
            raise ApplicationError(f"Package with ID {package_id} start location "
                                   f"does not exists in Route with ID {route_id}")

        package.departure_time = route.departure_time
        package.estimated_arrival_time = route.stops[package.end_location]
        package.route_id = route.id
        package.is_assigned = True
        route.assign_package(package.id)
        route.load += package.weight

    def unassign_package_from_route(self, package_id: int, route_id: int):
        """
        Unassigns a package from its assigned route.

        Args:
            package_id (int): The ID of the package to unassign.
            route_id (int): The ID of the route to unassign the package from.

        Raises:
            ApplicationError: If the package or route does not exist, or if the package is not assigned to the route.
        """
        package = self.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")

        route = self.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")
        if route.departure_time > ApplicationTime.current():
            raise ApplicationError(f"Assigned Truck to Route with ID {route_id} has already departed")

        package.departure_time = None
        package.estimated_arrival_time = None
        package.route_id = None
        package.is_assigned = False
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
        Finds a truck by its ID.

        Args:
            truck_id (int): The ID of the truck to find.

        Returns:
            Truck: The truck with the specified ID, or `None` if no truck is found.
        """
        return next((truck for truck in self.trucks if truck.id == truck_id), None)

    def find_route_by_id(self, route_id: int) -> Route:
        """
        Finds a route by its ID.

        Args:
            route_id (int): The ID of the route to find.

        Returns:
            Route: The route with the specified ID, or `None` if no route is found.
        """
        return next((route for route in self.routes if route.id == route_id), None)

    def find_package_by_id(self, package_id: int) -> Package:
        """
        Finds a package by its ID.

        Args:
            package_id (int): The ID of the package to find.

        Returns:
            Package: The package with the specified ID, or `None` if no package is found.
        """
        return next((package for package in self.packages if package.id == package_id), None)

    def find_employee_by_username(self, username: str) -> Employee:
        """
        Finds an employee by their username.

        Args:
            username (str): The username of the employee to find.

        Returns:
            Employee: The employee with the specified username, or `None` if no employee is found.
        """
        return next((employee for employee in self.employees if employee.username == username), None)

    def login(self, employee: Employee):
        """
        Logs in an employee by setting them as the currently logged-in employee.

        Args:
            employee (Employee): The employee to log in.
        """
        self._logged_in_employee = employee

    def logout(self):
        """
        Logs out the currently logged-in employee by setting the logged-in employee to `None`.
        After calling this method, no employee will be considered logged in until a new `login` method is called.
        """
        self._logged_in_employee = None
