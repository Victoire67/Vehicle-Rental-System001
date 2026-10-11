import pytest

from rental_system import RentalError, RentalSystem

DETAILS = dict(make="Toyota", model="Corolla", year=2020,
               registration="RAD 123 A", daily_rate=50)


@pytest.fixture
def system(tmp_path):
    return RentalSystem(tmp_path / "vehicles.json")


# Deleting a car removes it completely from the cars list
def test_delete_removes_car_from_list(system):
    car = system.add_vehicle("car", **DETAILS)
    system.delete(car.vehicle_id)
    assert car not in system.vehicles


def test_delete_removes_car_from_file(system):
    car = system.add_vehicle("car", **DETAILS)
    system.delete(car.vehicle_id)
    reloaded = RentalSystem(system.path)
    assert reloaded.vehicles == []


# Once a car is deleted, it cannot be available
def test_deleted_car_is_not_available(system):
    car = system.add_vehicle("car", **DETAILS)
    system.delete(car.vehicle_id)
    assert car not in system.available_vehicles()
    assert system.available_count() == 0


def test_deleted_car_cannot_be_rented(system):
    car = system.add_vehicle("car", **DETAILS)
    system.delete(car.vehicle_id)
    with pytest.raises(RentalError):
        system.rent(car.vehicle_id, "Aline")


# A car that is in use cannot be deleted
def test_cannot_delete_a_car_in_use(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    with pytest.raises(RentalError):
        system.delete(car.vehicle_id)
    assert car in system.vehicles


def test_delete_only_removes_the_chosen_car(system):
    first = system.add_vehicle("car", **DETAILS)
    second = system.add_vehicle("car", **DETAILS)
    system.delete(first.vehicle_id)
    assert system.vehicles == [second]


def test_cannot_delete_unknown_id(system):
    with pytest.raises(RentalError):
        system.delete("does-not-exist")