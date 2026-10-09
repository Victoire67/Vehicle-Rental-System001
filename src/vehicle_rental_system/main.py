from rental_system import RentalError, RentalSystem

MENU = """
1. Upload a vehicle
2. Show available vehicles
3. Rent a vehicle
0. Quit
"""

EXTRA_QUESTIONS = {
    "car": ("seats", "Number of seats: "),
    "bike": ("bike_type", "Bike type (road/mountain/electric): "),
    "truck": ("load_capacity", "Load capacity in tonnes: "),
}


def upload(system):
    kind = input("Type (car/bike/truck): ").strip().lower()
    if kind not in EXTRA_QUESTIONS:
        raise RentalError("Type must be car, bike or truck.")
    details = {
        "make": input("Make: ").strip(),
        "model": input("Model: ").strip(),
        "year": input("Year: ").strip(),
        "registration": input("Registration: ").strip(),
        "daily_rate": input("Daily rate: ").strip(),
    }
    field, question = EXTRA_QUESTIONS[kind]
    details[field] = input(question).strip()
    vehicle = system.add_vehicle(kind, **details)
    print(f"Added: {vehicle}")
    print(f"Vehicles available now: {system.available_count()}")


def show(vehicles):
    if not vehicles:
        print("Nothing to show.")
    for vehicle in vehicles:
        print(vehicle)


def main():
    system = RentalSystem()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                upload(system)
            elif choice == "2":
                show(system.available_vehicles())
            elif choice == "3":
                show(system.available_vehicles())
                vehicle_id = input("Vehicle id: ").strip()
                customer = input("Your name: ").strip()
                days = int(input("How many days? "))
                vehicle = system.rent(vehicle_id, customer)
                print(f"Rented: {vehicle}")
                print(f"Cost for {days} days: {vehicle.rental_cost(days):.2f}")
            elif choice == "0":
                break
            else:
                print("Please choose a number from the menu.")

        except (RentalError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
