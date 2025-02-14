import json
import os


class Location:
    CITIES = [
        "SYD",
        "MEL",
        "ADL",
        "ASP",
        "BRI",
        "DAR",
        "PER",
    ]

    @staticmethod
    def get_distance(city_1, city_2):
        file_path = os.path.join(os.path.dirname(__file__), "json/distances.json")

        with open(file_path, "r") as distances:
            distance_data = json.loads(distances.read())
        return distance_data[city_1][0][city_2]