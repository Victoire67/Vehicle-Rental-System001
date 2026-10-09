import pytest

from rental_system import RentalError, RentalSystem

DETAILS = dict(make="Toyota", model="Corolla", year=2020,
               registration="RAD 123 A", daily_rate=50)


@pytest.fixture
def system(tmp_path):
    return RentalSystem(tmp_path / "vehicles.json")


# A user can see a car
def test_uploaded_car_appears_in_available_list(system):
    car = system.add_vehicle("car", **DETAILS)
    assert car in system.available_vehicles()


# A user can rent a car, and its state changes to in use
def test_rent_changes_status_to_in_use(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    assert car.status == "in use"
    assert car.rented_by == "Aline"


def test_rented_car_is_not_in_available_list(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    assert car not in system.available_vehicles()
    assert system.available_count() == 0


def test_rented_status_is_saved_to_file(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    reloaded = RentalSystem(system.path)
    assert reloaded.vehicles[0].status == "in use"


def test_cannot_rent_a_car_already_in_use(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    with pytest.raises(RentalError):
        system.rent(car.vehicle_id, "Eric")


def test_cannot_rent_unknown_id(system):
    with pytest.raises(RentalError):
        system.rent("does-not-exist", "Aline")