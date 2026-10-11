# Vehicle Rental System
e
A command-line vehicle rental system written in Python. users can list cars, bikes, and trucks for rent, and users can rent, return, book, and delete them. All data is saved locally in a JSON file.

## Features

| Feature | What it does |
|---|---|
| Upload a vehicle | Adds a car, bike, or truck with a unique id and saves it to the data file |
| Show available vehicles | Lists the vehicles that can be rented right now |
| Rent a vehicle | Changes a vehicle's status from "available" to "in use" and shows the cost |
| Return a vehicle | Changes a vehicle's status back to "available" |
| Show all vehicles | Lists every vehicle, including those in use |
| Delete a vehicle | Removes a vehicle completely (not allowed while it is in use) |
| Book a vehicle | Reserves a vehicle for one customer from a future date |

## Requirements

- Python 3.10 or newer
- [Poetry](https://python-poetry.org/)

## Setup

```bash
git clone <repository url>
cd vehicle-rental-system
poetry install
```

## Usage

Run these commands from the folder that contains `main.py`.

```bash
poetry run python main.py
```

You will see this menu:

```
1. Upload a vehicle
2. Show available vehicles
3. Rent a vehicle
4. Return a vehicle
5. Show all vehicles
6. Delete a vehicle
7. Book a vehicle for later
0. Quit
```

Type the number of an option and press Enter. Each vehicle is shown on one line:

```
[3f2b8c1e] Car | 2020 Toyota Corolla | 50.00/day | available
```

The value in square brackets is the vehicle id. Use it when renting, returning, deleting, or booking.

## Vehicle types and pricing

Every vehicle has a make, model, year, registration, and daily rate. Each type adds one attribute of its own and calculates the rental cost differently.

| Type | Extra attribute | Rental cost |
|---|---|---|
| Car | Number of seats | daily rate x days |
| Bike | Bike type (road, mountain, electric) | daily rate x days, with 10% off for 7 days or more |
| Truck | Load capacity in tonnes | (daily rate + 5 x load capacity) x days |

The daily rate is a plain number greater than 0, such as `50` or `49.99`. No currency is stored.

## How booking works

- A vehicle can be booked whether it is available or in use.
- Before the booked date, anyone can still rent it.
- From the booked date onward, only the customer who booked it can rent it.
- When that customer rents it, the booking is cleared.

## Data storage

Vehicles are saved in `data/vehicles.json`, which is created the first time a vehicle is uploaded. The file is rewritten after every change, so it always matches what the program shows.

The `data/` folder is listed in `.gitignore`, so local data is not committed.

## Project structure

```
vehicles.py          Vehicle base class and the Car, Bike, and Truck subclasses
storage.py           Loads and saves vehicles to the JSON file
rental_system.py     The rules: upload, rent, return, delete, book
main.py              The command-line menu
tests/
    test_upload.py
    test_rent.py
    test_return.py
    test_delete.py
    test_book.py
```

## Design

- **Inheritance:** `Car`, `Bike`, and `Truck` inherit shared attributes and behaviour from the abstract `Vehicle` class.
- **Properties:** `daily_rate` is a property whose setter converts the value to a number and rejects zero or negative rates. `is_available` is a read-only property computed from the status.
- **Polymorphism:** Each subclass provides its own `rental_cost(days)` and `extra_fields()`. The rest of the program calls these on any vehicle without checking its type.
- **Extensibility:** A new vehicle type needs one new subclass and one entry in `VEHICLE_TYPES`. The rental rules do not change.


