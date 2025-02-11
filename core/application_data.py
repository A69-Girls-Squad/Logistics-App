from datetime import datetime
from models.truck import Truck
from models.package import Package
from models.route import Route
from models.user_role import UserRole


class ApplicationData:
    def __init__(self):
        self._trucks = []
        self._routes = []
        self._packages = []

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
    def not_assigned_packages(self):
        not_assigned_packages = []
        for package in self.packages:
            if not package.is_assigned:
                not_assigned_packages.append(package)
        return not_assigned_packages

    @property
    def logged_in_user(self):
        pass

    @property
    def users(self):
        pass

    def create_package(self, start_location: str, end_location: str, weight: float, customer_email: str):
        package = Package(start_location, end_location, weight, customer_email)
        self._packages.append(package)

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

    def create_user(self, username: str, firstname: str, lastname: str, password: str, user_role: UserRole):
        pass

    def login(self, user):
        pass

    def logout(self):
        pass

    def register_user(self):
        pass

    def find_user_by_username(self, username):
        pass