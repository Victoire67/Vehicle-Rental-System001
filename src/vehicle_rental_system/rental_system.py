from storage import DATA_FILE, load_vehicles, save_vehicles
from vehicles import VEHICLE_TYPES

REQUIRED_FIELDS = ["make", "model", "year", "registration", "daily_rate"]


class RentalError(Exception):
    """Raised when a rental rule is broken."""


class RentalSystem:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.vehicles = load_vehicles(path)

    def _save(self):
        save_vehicles(self.vehicles, self.path)

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