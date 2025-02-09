class Location:

    CITIES = {
        "SYD": 0,
        "MEL": 1,
        "ADL": 2,
        "ASP": 3,
        "BRI": 4,
        "DAR": 5,
        "PER": 6
    }

    DISTANCES = [
        [0, 877, 1376, 2762, 909, 3935, 4016],
        [877, 0, 725, 2255, 1765, 3752, 3509],
        [1376, 725, 0, 1530, 1927, 3027, 2785],
        [2762, 2255, 1530, 0, 2993, 1497, 2481],
        [909, 1765, 1927, 2993, 0, 3426, 4311],
        [3935, 3752, 3027, 1497, 3426, 0, 4025],
        [4016, 3509, 2785, 2481, 4311, 4025, 0]
    ]

    # To implement JSON file
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    def get_distance(self, city_1, city_2):
        return self.DISTANCES[self.CITIES[city_1][self.CITIES[city_2]]]