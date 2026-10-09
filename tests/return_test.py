import pytest

from rental_system import RentalError, RentalSystem

DETAILS = dict(make="Toyota", model="Corolla", year=2020,
               registration="RAD 123 A", daily_rate=50)


@pytest.fixture
def system(tmp_path):
    return RentalSystem(tmp_path / "vehicles.json")


@pytest.fixture
def rented_car(system):
    car = system.add_vehicle("car", **DETAILS)
    system.rent(car.vehicle_id, "Aline")
    return car


# Car successfully returned, and shows status "Available"
def test_return_makes_car_available(system, rented_car):
    system.return_vehicle(rented_car.vehicle_id)
    assert rented_car.status == "available"
    assert rented_car.rented_by is None


def test_returned_car_is_back_in_available_list(system, rented_car):
    system.return_vehicle(rented_car.vehicle_id)
    assert rented_car in system.available_vehicles()


def test_returned_car_can_be_rented_again(system, rented_car):
    system.return_vehicle(rented_car.vehicle_id)
    system.rent(rented_car.vehicle_id, "Eric")
    assert rented_car.rented_by == "Eric"


def test_returned_status_is_saved_to_file(system, rented_car):
    system.return_vehicle(rented_car.vehicle_id)
    reloaded = RentalSystem(system.path)
    assert reloaded.vehicles[0].status == "available"


def test_cannot_return_a_car_that_is_not_rented(system):
    car = system.add_vehicle("car", **DETAILS)
    with pytest.raises(RentalError):
        system.return_vehicle(car.vehicle_id)