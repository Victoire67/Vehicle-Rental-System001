import json
from pathlib import Path

from vehicles import vehicle_from_dict

DATA_FILE = Path("data") / "vehicles.json"


def load_vehicles(path=DATA_FILE):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as file:
        return [vehicle_from_dict(item) for item in json.load(file)]


def save_vehicles(vehicles, path=DATA_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump([v.to_dict() for v in vehicles], file, indent=2)