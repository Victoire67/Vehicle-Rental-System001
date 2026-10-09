import uuid
from abc import ABC, abstractmethod

AVAILABLE = "available"
IN_USE = "in use"


class Vehicle(ABC):
    kind = "vehicle"

    def __init__(self, make, model, year, registration, daily_rate,
                 vehicle_id=None, status=AVAILABLE, rented_by=None, booking=None):
        self.vehicle_id = vehicle_id or uuid.uuid4().hex[:8]
        self.make = make
        self.model = model
        self.year = int(year)
        self.registration = registration
        self.daily_rate = daily_rate   # runs the setter below
        self.status = status
        self.rented_by = rented_by
        self.booking = booking         # None, or {"customer": ..., "start": "2026-10-20"}

    @property
    def daily_rate(self):
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Daily rate must be greater than 0.")
        self._daily_rate = value

    @property
    def is_available(self):
        return self.status == AVAILABLE

    @abstractmethod
    def rental_cost(self, days):
        """Each vehicle type must say how its price is calculated."""

    def extra_fields(self):
        return {}

    def to_dict(self):
        data = {
            "kind": self.kind,
            "vehicle_id": self.vehicle_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "registration": self.registration,
            "daily_rate": self.daily_rate,
            "status": self.status,
            "rented_by": self.rented_by,
            "booking": self.booking,
        }
        data.update(self.extra_fields())
        return data

    def __str__(self):
        return (f"[{self.vehicle_id}] {self.kind.title()} | {self.year} "
                f"{self.make} {self.model} | {self.daily_rate:.2f}/day | {self.status}")


class Car(Vehicle):
    kind = "car"

    def __init__(self, make, model, year, registration, daily_rate, seats=5, **kwargs):
        super().__init__(make, model, year, registration, daily_rate, **kwargs)
        self.seats = int(seats)

    def rental_cost(self, days):
        return self.daily_rate * days

    def extra_fields(self):
        return {"seats": self.seats}


class Bike(Vehicle):
    kind = "bike"

    def __init__(self, make, model, year, registration, daily_rate, bike_type="road", **kwargs):
        super().__init__(make, model, year, registration, daily_rate, **kwargs)
        self.bike_type = bike_type

    def rental_cost(self, days):
        cost = self.daily_rate * days
        if days >= 7:
            cost *= 0.9            # 10% off for a week or more
        return cost

    def extra_fields(self):
        return {"bike_type": self.bike_type}


class Truck(Vehicle):
    kind = "truck"

    def __init__(self, make, model, year, registration, daily_rate, load_capacity=1, **kwargs):
        super().__init__(make, model, year, registration, daily_rate, **kwargs)
        self.load_capacity = float(load_capacity)

    def rental_cost(self, days):
        return (self.daily_rate + 5 * self.load_capacity) * days

    def extra_fields(self):
        return {"load_capacity": self.load_capacity}


VEHICLE_TYPES = {"car": Car, "bike": Bike, "truck": Truck}


def vehicle_from_dict(data):
    data = dict(data)              # copy, so the original isn't changed
    kind = data.pop("kind")
    return VEHICLE_TYPES[kind](**data)