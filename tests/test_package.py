import unittest
from models.package import Package
from errors.application_error import ApplicationError
import test_data as td
from datetime import datetime

class PackageTests(unittest.TestCase):
    def setUp(self):
        """Reset the ID counter before each test."""
        Package._current_id = 0

    def test_createPackage_withValidData_returnsValidPackage(self):
        # Arrange
        # Act
        package = Package(
            start_location=td.VALID_START_LOCATION,
            end_location=td.VALID_END_LOCATION,
            weight=td.VALID_WEIGHT,
            customer_email=td.VALID_CUSTOMER_EMAIL
        )

        # Assert
        self.assertEqual(package.id, 1)
        self.assertEqual(package.start_location, td.VALID_START_LOCATION)
        self.assertEqual(package.end_location, td.VALID_END_LOCATION)
        self.assertEqual(package.weight, td.VALID_WEIGHT)
        self.assertEqual(package.customer_email, td.VALID_CUSTOMER_EMAIL)
        self.assertIsNone(package.departure_time)
        self.assertIsNone(package.estimated_arrival_time)
        self.assertFalse(package.is_assigned)
        self.assertIsNone(package.route_id)

    def test_createPackage_withInvalidStartLocation_raisesValueError(self):
        # Arrange
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Package(
                start_location=td.INVALID_START_LOCATION,
                end_location=td.VALID_END_LOCATION,
                weight=td.VALID_WEIGHT,
                customer_email=td.VALID_CUSTOMER_EMAIL
            )
        self.assertEqual(str(context.exception), "Start location does not exist")

    def test_createPackage_withInvalidEndLocation_raisesValueError(self):
        # Arrange
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Package(
                start_location=td.VALID_START_LOCATION,
                end_location=td.INVALID_END_LOCATION,
                weight=td.VALID_WEIGHT,
                customer_email=td.VALID_CUSTOMER_EMAIL
            )
        self.assertEqual(str(context.exception), "End location does not exist")

    def test_createPackage_withSameStartAndEndLocation_raisesApplicationError(self):
        # Arrange
        # Act & Assert
        with self.assertRaises(ApplicationError) as context:
            Package(
                start_location=td.VALID_START_LOCATION,
                end_location=td.VALID_START_LOCATION,
                weight=td.VALID_WEIGHT,
                customer_email=td.VALID_CUSTOMER_EMAIL
            )
        self.assertEqual(str(context.exception), "Start location can not be the same as End location")

    def test_createPackage_withNegativeWeight_raisesValueError(self):
        # Arrange
        negative_weight = -5

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Package(
                start_location=td.VALID_START_LOCATION,
                end_location=td.VALID_END_LOCATION,
                weight=negative_weight,
                customer_email=td.VALID_CUSTOMER_EMAIL
            )
        self.assertEqual(str(context.exception), "Weight can not be a negative number")

    def test_createPackage_withInvalidEmail_raisesValueError(self):
        # Arrange
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Package(
                start_location=td.VALID_START_LOCATION,
                end_location=td.VALID_END_LOCATION,
                weight=td.VALID_WEIGHT,
                customer_email=td.INVALID_CUSTOMER_EMAIL
            )
        self.assertEqual(str(context.exception), f"Invalid email address: {td.INVALID_CUSTOMER_EMAIL}")

    def test_fromJson_withValidData_returnsValidPackage(self):
        # Arrange
        json_data = {
            "start_location": td.VALID_START_LOCATION,
            "end_location": td.VALID_END_LOCATION,
            "weight": td.VALID_WEIGHT,
            "customer_email": td.VALID_CUSTOMER_EMAIL,
            "departure_time": td.VALID_DEPARTURE_TIME_INPUT,
            "estimated_arrival_time": td.VALID_DEPARTURE_TIME_OUTPUT.isoformat(),
            "is_assigned": True,
            "route_id": 1
        }

        # Act
        package = Package.from_json(json_data)

        # Assert
        self.assertEqual(package.start_location, td.VALID_START_LOCATION)
        self.assertEqual(package.end_location, td.VALID_END_LOCATION)
        self.assertEqual(package.weight, td.VALID_WEIGHT)
        self.assertEqual(package.customer_email, td.VALID_CUSTOMER_EMAIL)
        self.assertEqual(package.departure_time, td.VALID_DEPARTURE_TIME_OUTPUT)
        self.assertEqual(package.estimated_arrival_time, td.VALID_ESTIMATED_ARRIVAL_TIME_OUTPUT)
        self.assertTrue(package.is_assigned)
        self.assertEqual(package.route_id, 1)

    def test_toJson_returnsValidJson(self):
        # Arrange
        package = Package(
            start_location=td.VALID_START_LOCATION,
            end_location=td.VALID_END_LOCATION,
            weight=td.VALID_WEIGHT,
            customer_email=td.VALID_CUSTOMER_EMAIL
        )
        package.departure_time = td.VALID_DEPARTURE_TIME_OUTPUT
        package.estimated_arrival_time = td.VALID_ESTIMATED_ARRIVAL_TIME_OUTPUT
        package.is_assigned = True
        package.route_id = 1

        # Act
        json_data = package.to_json()

        # Assert
        self.assertEqual(json_data["id"], 1)
        self.assertEqual(json_data["start_location"], td.VALID_START_LOCATION)
        self.assertEqual(json_data["end_location"], td.VALID_END_LOCATION)
        self.assertEqual(json_data["weight"], td.VALID_WEIGHT)
        self.assertEqual(json_data["customer_email"], td.VALID_CUSTOMER_EMAIL)
        self.assertEqual(json_data["departure_time"], td.VALID_DEPARTURE_TIME_OUTPUT.isoformat())
        self.assertEqual(json_data["estimated_arrival_time"], td.VALID_ESTIMATED_ARRIVAL_TIME_OUTPUT.isoformat())
        self.assertTrue(json_data["is_assigned"])
        self.assertEqual(json_data["route_id"], 1)

    def test_str_returnsValidStringRepresentation(self):
        # Arrange
        package = Package(
            start_location=td.VALID_START_LOCATION,
            end_location=td.VALID_END_LOCATION,
            weight=td.VALID_WEIGHT,
            customer_email=td.VALID_CUSTOMER_EMAIL
        )
        package.departure_time = td.VALID_DEPARTURE_TIME_OUTPUT
        package.estimated_arrival_time = td.VALID_ESTIMATED_ARRIVAL_TIME_OUTPUT

        expected_output = (
            f"ID: 1\n"
            f"Start Location: {td.VALID_START_LOCATION}\n"
            f"End Location: {td.VALID_END_LOCATION}\n"
            f"Weight: {td.VALID_WEIGHT:.2f} kg\n"
            f"Customer Email Address: {td.VALID_CUSTOMER_EMAIL}\n"
            f"Package status: Awaiting Dispatch\n"
            f"Departure time: {td.VALID_DEPARTURE_TIME_OUTPUT.isoformat(sep=' ', timespec='minutes')}\n"
            f"Estimated arrival time: {td.VALID_ESTIMATED_ARRIVAL_TIME_OUTPUT.isoformat(sep=' ', timespec='minutes')}"
        )

        # Act
        result = str(package)

        # Assert
        self.assertEqual(result, expected_output)