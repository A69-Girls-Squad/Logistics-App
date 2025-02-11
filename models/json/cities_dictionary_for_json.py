import json


cities = {
    "Cities": [
        {
            "SYD": 0,
            "MEL": 1,
            "ADL": 2,
            "ASP": 3,
            "BRI": 4,
            "DAR": 5,
            "PER": 6
        }
    ]
        }

json_string = json.dumps(cities)
with open('cities.json', 'w') as f:
    f.write(json_string)