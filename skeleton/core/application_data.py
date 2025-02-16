from datetime import datetime

from skeleton.models.employee import Employee
from skeleton.models.truck import Truck
from skeleton.models.package import Package
from skeleton.models.route import Route


class ApplicationData:

    def __init__(self):
        self._trucks = []
        self._routes = []
        self._packages = []
        self._employee = []
        self._logged_employee = None

    @property
    def trucks(self):
        return self._trucks

    @property
    def routes(self):
        return self._routes

    @property
    def packages(self):
        return self._packages

    @property
    def employees(self):
        return self._employee

    @property
    def not_assigned_packages(self):
        not_assigned_packages = []
        for package in self.packages:
            if not package.is_assigned:
                not_assigned_packages.append(package)
        return not_assigned_packages

    @property
    def logged_in_employee(self):
        if self.has_logged_in_employee:
            return self._logged_employee
        else:
            raise ValueError('There is no logged in employee.')

    @property
    def has_logged_in_employee(self):
        return self._logged_employee is not None

    def create_package(self, start_location: str, end_location: str, weight: float, customer_email: str) -> Package:
        package = Package(start_location, end_location, weight, customer_email)
        self._packages.append(package)
        return package

    def create_route(self, id, locations: list[str], departure_time: datetime):
        route = Route(id, locations, departure_time)
        self._routes.append(route)

    def find_package_by_id(self, id) -> Package:
        for package in self.packages:
            if package.id == id:
                return package

    def find_route_by_id(self, id) -> Route:
        for route in self.routes:
            if route.id == id:
                return route

    def find_truck_by_id(self, id) -> Truck:
        for truck in self.trucks:
            if truck.id == id:
                return truck

    def create_employee(self, username, firstname, lastname, password, employee_role) -> Employee:
        if len([u for u in self._employee if u.username == username]) > 0:
            raise ValueError(
                f'Employee {username} already exist. Choose a different username!')

        employee = Employee(username, firstname, lastname, password, employee_role)
        self._employee.append(employee)

        return employee

    def find_employee_by_username(self, username: str) -> Employee:
        filtered = [employee for employee in self._employee if employee.username == username]
        if not filtered:
            raise ValueError(f'There is no employee with username {username}!')

        return filtered[0]

    def login(self, employee: Employee):
        self._logged_employee = employee

    def logout(self):
        self._logged_employee = None

    def get_packages_by_assigned_status(self, is_assigned: bool) -> list:
        result = []
        for package in self._packages:
            if package.is_assigned == is_assigned:
                result.append(package)

        return result