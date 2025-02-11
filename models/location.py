import json


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
        with open("distances.json", "r") as distances:
            distance_data = json.loads(distances.read())
        return distance_data[city_1][0][city_2]