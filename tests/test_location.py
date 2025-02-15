import unittest
from unittest.mock import patch
import test_data as td
from models.location import Location


class Location_Should(unittest.TestCase):

    @patch("builtins.print")
    def test_get_distance_invalidCity_1(self, mock_print):
        Location.get_distance(td.INVALID_CITY, td.VALID_CITY_2)
        mock_print.assert_called_with(f"Invalid city: {td.INVALID_CITY}")

    @patch("builtins.print")
    def test_get_distance_invalidCity_2(self, mock_print):
        Location.get_distance(td.VALID_CITY_1, td.INVALID_CITY)
        mock_print.assert_called_with(f"Invalid city: {td.INVALID_CITY}")

    @patch("builtins.print")
    def test_get_distance_equalCities(self, mock_print):
        Location.get_distance(td.VALID_CITY_1, td.VALID_CITY_1)
        mock_print.assert_called_with("Cities cannot be the same!")

    def test_get_distance_returnsCorrect(self):
        distance = Location.get_distance(td.VALID_CITY_1, td.VALID_CITY_2)
        self.assertEqual(td.EXPECTED_DISTANCE, distance)