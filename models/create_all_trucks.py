from models.truck import Truck

def create_all_trucks():
    all_trucks = []
    # (Name, Capacity, Max Range, Number of trucks)
    description = [("Scania", 42000, 8000, 10), ("Man", 37000, 10000, 15), ("Actros", 26000, 13000, 15)]


    for name, capacity, max_range, number_of_trucks in description:
        for i in range(number_of_trucks):
            all_trucks.append(Truck(name, capacity, max_range))

    return all_trucks


trucks = create_all_trucks()
for truck in trucks:
    print(truck)
