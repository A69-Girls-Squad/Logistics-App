class Distance:

    DISTANCES = {
        "SYD": {
            "MEL": 877,
            "ADL": 1376,
            "ASP": 2762,
            "BRI": 909,
            "DAR": 3935,
            "PER": 4016
        },
        "MEL": {
            "SYD": 877,
            "ADL": 725,
            "ASP": 2255,
            "BRI": 1765,
            "DAR": 3752,
            "PER": 3509
        },
        "ADL": {
            "SYD": 1376,
            "MEL": 725,
            "ASP": 1530,
            "BRI": 1927,
            "DAR": 3027,
            "PER": 2785
        },
        "ASP": {
            "SYD": 2762,
            "MEL": 2255,
            "ADL": 1530,
            "BRI": 2993,
            "DAR": 1497,
            "PER": 2481
        },
        "BRI": {
            "SYD": 909,
            "MEL": 1765,
            "ADL": 1927,
            "ASP": 2993,
            "DAR": 3426,
            "PER": 4311
        },
        "DAR": {
            "SYD": 3935,
            "MEL": 3752,
            "ADL": 3027,
            "ASP": 1497,
            "BRI": 3426,
            "PER": 4025
        },
        "PER": {
            "SYD": 4016,
            "MEL": 3509,
            "ADL": 2785,
            "ASP": 2481,
            "BRI": 4311,
            "DAR": 4025
        }
    }

    @classmethod
    def get_distance(cls, city_1: str, city_2: str) -> int:
        """
        Retrieves the distance between two cities from a pre-defined JSON file.

        Parameters:
        - `city_1` (str): The name of the starting city.
        - `city_2` (str): The name of the destination city.

        Returns:
        - `float | int`: The distance between `city_1` and `city_2` as stored in the JSON file.
        """
        return cls.DISTANCES[city_1][city_2]

