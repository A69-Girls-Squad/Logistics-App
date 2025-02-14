import unittest
import uuid
from datetime import datetime

import test_data as td
from models.route import Route


class Route_Should(unittest.TestCase):

    def test_init(self):
        route = Route(td.VALID_LOCATIONS, td.VALID_DEPARTURE_TIME)

        self.assertIsInstance(route.locations, tuple)
        self.assertIsInstance(route.departure_time, datetime)
        self.assertIsInstance(route.id, str)
        self.assertEqual(td.VALID_ID_LEN, len(route.id))
        self.assertEqual(None, route.assigned_truck)
        self.as