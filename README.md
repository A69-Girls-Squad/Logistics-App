# Logistics App

## Overview
The **Logistics App** is a console-based application designed to manage the delivery of packages between hubs in major Australian cities. It is intended for use by logistics company employees to record package details, create delivery routes, assign trucks, and track delivery statuses.

## Features
### Core Functionalities
#### Package Management:
- Create delivery packages with unique IDs, start and end locations, weight, and customer contact information.
- Assign packages to delivery routes.
- View package details and status (e.g., awaiting dispatch, in transit, delivered).

#### Route Management:
- Create delivery routes with unique IDs, a list of locations, departure times, and estimated arrival times.
- Search for suitable routes based on package start and end locations.
- Assign trucks to routes and update route details.

#### Truck Management:
- View available trucks and their details (capacity, max range, etc.).
- Assign trucks to routes based on capacity and range requirements.

#### Employee Management:
- Register and log in employees with different roles (e.g., Regular, Supervisor, Manager).
- Restrict certain actions based on employee roles.

#### Data Persistence:
- Save the application state to a JSON file for future use.

## Use Cases
### 1. Package Delivery
A customer visits the company office in Sydney on Oct 8th. They bring a package that needs to be delivered to Melbourne. An employee of the company records the customer’s contact info, weighs the package at 45kg and then checks for a suitable delivery route. The system reports that there are two routes:

- Brisbane (Oct 10th 06:00h) → Sydney (Oct 10th 20:00h) → Melbourne (Oct 11th 18:00h)

- Sydney (Oct 12th 06:00h) → Melbourne (Oct 12th 20:00h) → Adelaide (Oct 13th 15:00h)

Both routes' trucks have free capacity, and the employee suggests the first one, as the package will arrive one day earlier. The customer agrees and the employee uses the system to add the delivery package to the first route and to update the package’s expected arrival time to Oct 11th 18:00h.
### 2. Bulk Package Assignment
Many packages with total weight of 23000kg have gathered in the hub in Alice Springs and an employee of the company uses the system to create a route that leaves on Sep 12th 06:00h with the following stops:

- Alice Springs → Adelaide → Melbourne → Sydney → Brisbane

The system determines the route distance to 4041km and calculates estimated arrival times for each of the locations based on a predefined average speed of 87km/h. The employee then finds a free truck that meets the required range and capacity and proceeds to bulk assign the packages to the newly created route by using the route id and the packages’ ids
### 3. Route Inspection
A manager at the company uses the system to find information about all delivery routes in progress. The system responds with information that contains each route’s stops, delivery weight, and the expected current stop based on the time of the day.
### 4. Unassigned Packages
A supervising employee uses the system to view information about each package that is not yet assigned to a delivery route. The system responds with a list of packages containing their IDs and locations
### 5. Customer Inquiry
A customer contacts the office to request information about their package. The customer provides the id that they received when the package was created, and an employee enters the package id in the system. It responds with detailed information which is then emailed to the customer.
## Models
### Key Classes
#### Employee:
- Represents an employee with a username, first name, last name, password, and role.
- **Roles:** Regular, Supervisor, Manager.

#### Package:
- Represents a delivery package with a unique ID, start location, end location, weight, customer email, and tracking information (departure time, estimated arrival time, and assignment status).

#### Route:
- Represents a delivery route with a unique ID, list of locations, departure time, assigned truck, packages, and estimated arrival times.
- Calculates the total distance and estimated arrival times for each stop.

#### Truck:
- Represents a delivery truck with a unique ID, name, capacity, max range, and assigned route.
- Checks if a truck is suitable for a route based on capacity and range.

## Installation
### Prerequisites:
- Python 3.x installed on your system.
- Git (optional, for version control).

### Clone the Repository:
```bash
git clone https://github.com/your-repo/logistics-app.git
cd logistics-app
```

### Run the Application:
```bash
python main.py
```

## Usage
### Menu Options
The application provides a menu-driven interface with the following options:
```
==============================
            MENU
==============================
1. Register Employee
2. Login
3. Logout

4. Create Route
5. Create Package

6. Search for Suitable Route
7. Search for Suitable Truck

8. Assign Truck to Route
9. Remove Truck from Route
10. Assign Package to Route
11. Bulk Assign Packages
12. Reassign Package
13. Remove Package from Route

14. Show Employees
15. Show Package Info
16. Show Packages
17. Show Route Info
18. Show Routes
19. Show All Trucks
------------------------------
FOR EXIT TYPE "exit"
------------------------------
To see MENU press Enter
or to enter a command, type a number: 
```

### Example Usage
#### Show Packages Info
```
Enter command: 16

------------------------------
SHOW PACKAGES INFO:
------------------------------
Please, choose which packages you would like to see:
------------------------------
assigned
unassigned
all
------------------------------

Status: unassigned
You are not logged in! Please login first!
============================================================
```

#### Login
```
Enter command: 2

------------------------------
LOGIN:
------------------------------

Username: eerie007
Password: welcome123@

Employee eerie007 successfully logged in!
```

#### View Unassigned Packages
```
Enter command: 16

------------------------------
SHOW PACKAGES INFO:
------------------------------
Please, choose which packages you would like to see:
------------------------------
assigned
unassigned
all
------------------------------

Status: unassigned

============================================================
PACKAGES:
============================================================
PACKAGE DETAILS:
----------------|-------------------------------------------
ID:             | 3
----------------|-------------------------------------------
Start Location: | SYD
----------------|-------------------------------------------
End Location:   | MEL
----------------|-------------------------------------------
Weight:         | 45.00 kg
----------------|-------------------------------------------
Customer Email: | johnsmith@gmail.com
----------------|-------------------------------------------
Package Status: | Not assigned
----------------|-------------------------------------------
```

## JSON Data Structure

The application state is saved and loaded using JSON. Here's an example of the JSON structure:

```json
{
  "trucks": [
    {
      "id": 1001,
      "name": "Scania",
      "capacity": 42000,
      "max_range": 8000,
      "assigned_route_id": null
    }
  ],
  "routes": [
    {
      "id": 1,
      "locations": "SYD,MEL",
      "departure_time": "2023-10-10T06:00:00",
      "assigned_truck_id": null,
      "assigned_package_ids": [],
      "load": 0
    }
  ],
  "packages": [
    {
      "id": 1,
      "start_location": "SYD",
      "end_location": "MEL",
      "weight": 45,
      "customer_email": "customer@example.com",
      "departure_time": null,
      "estimated_arrival_time": null,
      "is_assigned": false,
      "route_id": null
    }
  ],
  "employees": [
    {
      "username": "employee1",
      "first_name": "John",
      "last_name": "Doe",
      "password": "password123",
      "employee_role": "REGULAR"
    }
  ]
}
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

## Contact

For questions or feedback, please contact:

- **Irina Parvanova:** parvanova.iri@gmail.com
- **Diana Valcheva:** diana.valcheva@gmail.com
- **Dilyana Bozhinova:** bozhinova.dilyana@gmail.com
- **Project Repository:** [GitHub Repo](https://github.com/A69-Girls-Squad/Logistics-App.git)


