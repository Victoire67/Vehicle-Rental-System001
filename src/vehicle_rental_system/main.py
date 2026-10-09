from rental_system import RentalError, RentalSystem

MENU = """
1. Upload a vehicle
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


def main():
    system = RentalSystem()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                upload(system)
            elif choice == "0":
                break
            else:
                print("Please choose a number from the menu.")
        except (RentalError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()