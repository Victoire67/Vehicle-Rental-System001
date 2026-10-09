import pytest

from rental_system import RentalError, RentalSystem
from vehicles import Bike, Car, Truck

DETAILS = dict(make="Toyota", model="Corolla", year=2020,
               registration="RAD 123 A", daily_rate=50)


@pytest.fixture
def system(tmp_path):
    return RentalSystem(tmp_path / "vehicles.json")


# A car can be created and stored in the appropriate file
def test_upload_saves_vehicle_to_file(system):
    system.add_vehicle("car", seats=5, **DETAILS)
    reloaded = RentalSystem(system.path)
    assert len(reloaded.vehicles) == 1
    assert reloaded.vehicles[0].make == "Toyota"
    assert reloaded.vehicles[0].seats == 5


# The owner can choose Car, Bike, or Truck
def test_can_upload_car_bike_and_truck(system):
    car = system.add_vehicle("car", seats=5, **DETAILS)
    bike = system.add_vehicle("bike", bike_type="road", **DETAILS)
    truck = system.add_vehicle("truck", load_capacity=4, **DETAILS)
    assert isinstance(car, Car)
    assert isinstance(bike, Bike)
    assert isinstance(truck, Truck)


def test_unknown_type_is_rejected(system):
    with pytest.raises(RentalError):
        system.add_vehicle("plane", **DETAILS)


# Every vehicle requires make, model, year, registration, and daily rate
def test_missing_field_is_rejected(system):
    with pytest.raises(RentalError):
        system.add_vehicle("car", **dict(DETAILS, make=""))


def test_invalid_daily_rate_is_rejected(system):
    with pytest.raises(ValueError):
        system.add_vehicle("car", **dict(DETAILS, daily_rate=-10))


# The uploaded car has a unique id
def test_each_vehicle_gets_a_unique_id(system):
    first = system.add_vehicle("car", **DETAILS)
    second = system.add_vehicle("car", **DETAILS)
    assert first.vehicle_id != second.vehicle_id


# Uploading updates the number of cars available
def test_upload_updates_available_count(system):
    assert system.available_count() == 0
    system.add_vehicle("car", **DETAILS)
    assert system.available_count() == 1