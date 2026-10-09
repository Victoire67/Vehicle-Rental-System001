from storage import DATA_FILE, load_vehicles, save_vehicles
from vehicles import VEHICLE_TYPES, IN_USE , AVAILABLE , VEHICLE_TYPES
from datetime import date
REQUIRED_FIELDS = ["make", "model", "year", "registration", "daily_rate"]


class RentalError(Exception):
    """Raised when a rental rule is broken."""


class RentalSystem:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.vehicles = load_vehicles(path)

    def _save(self):
        save_vehicles(self.vehicles, self.path)

        def find(self, vehicle_id):
          for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                return vehicle
        raise RentalError(f"No vehicle with id {vehicle_id}.")

    def available_vehicles(self):
        return [v for v in self.vehicles if v.is_available]

    def rent(self, vehicle_id, customer, today=None):
        today = today or date.today()
        vehicle = self.find(vehicle_id)
        if not vehicle.is_available:
            raise RentalError("That vehicle is already in use.")
        booking = vehicle.booking
        if booking and date.fromisoformat(booking["start"]) <= today:
            if booking["customer"] != customer:
                raise RentalError(
                    f"Reserved for {booking['customer']} from {booking['start']}.")
            vehicle.booking = None
        vehicle.status = IN_USE
        vehicle.rented_by = customer
        self._save()
        return vehicle

    def available_count(self):
        return len([v for v in self.vehicles if v.is_available])

    def add_vehicle(self, kind, **details):
        if kind not in VEHICLE_TYPES:
            raise RentalError("Type must be car, bike or truck.")
        for field in REQUIRED_FIELDS:
            if not str(details.get(field, "")).strip():
                raise RentalError(f"{field} is required.")
        vehicle = VEHICLE_TYPES[kind](**details)
        self.vehicles.append(vehicle)
        self._save()
        return vehicle
    def return_vehicle(self, vehicle_id):
        vehicle = self.find(vehicle_id)
        if vehicle.is_available:
            raise RentalError("That vehicle is not rented out.")
        vehicle.status = AVAILABLE
        vehicle.rented_by = None
        self._save()
        return vehicle
    def book(self, vehicle_id, customer, start, today=None):
        today = today or date.today()
        vehicle = self.find(vehicle_id)
        if vehicle.booking:
            raise RentalError("That vehicle already has a booking.")
        if start <= today:
            raise RentalError("The booking date must be in the future.")
        vehicle.booking = {"customer": customer, "start": start.isoformat()}
        self._save()
        return vehicle
