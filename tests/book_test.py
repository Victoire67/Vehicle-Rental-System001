from datetime import date

import pytest

from rental_system import RentalError, RentalSystem

DETAILS = dict(make="Toyota", model="Corolla", year=2020,
               registration="RAD 123 A", daily_rate=50)
TODAY = date(2026, 10, 9)
BOOKED_DAY = date(2026, 10, 20)


@pytest.fixture
def system(tmp_path):
    return RentalSystem(tmp_path / "vehicles.json")


@pytest.fixture
def car(system):
    return system.add_vehicle("car", **DETAILS)


# If a car is unavailable, it can be booked for a specific time
def test_can_book_a_car_that_is_in_use(system, car):
    system.rent(car.vehicle_id, "Aline", today=TODAY)
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    assert car.booking == {"customer": "Eric", "start": "2026-10-20"}


def test_booking_is_saved_to_file(system, car):
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    reloaded = RentalSystem(system.path)
    assert reloaded.vehicles[0].booking["customer"] == "Eric"


# Booking a car makes it available for you once it is the specified time
def test_booker_can_rent_on_the_booked_day(system, car):
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    system.rent(car.vehicle_id, "Eric", today=BOOKED_DAY)
    assert car.rented_by == "Eric"
    assert car.booking is None


def test_others_cannot_rent_on_the_booked_day(system, car):
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    with pytest.raises(RentalError):
        system.rent(car.vehicle_id, "Aline", today=BOOKED_DAY)
    assert car.status == "available"


def test_others_can_rent_before_the_booked_day(system, car):
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    system.rent(car.vehicle_id, "Aline", today=TODAY)
    assert car.rented_by == "Aline"
    assert car.booking is not None


def test_cannot_book_a_date_that_is_not_in_the_future(system, car):
    with pytest.raises(RentalError):
        system.book(car.vehicle_id, "Eric", TODAY, today=TODAY)


def test_cannot_book_a_car_that_is_already_booked(system, car):
    system.book(car.vehicle_id, "Eric", BOOKED_DAY, today=TODAY)
    with pytest.raises(RentalError):
        system.book(car.vehicle_id, "Aline", BOOKED_DAY, today=TODAY)