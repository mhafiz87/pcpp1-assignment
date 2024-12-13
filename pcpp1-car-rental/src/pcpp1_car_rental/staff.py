
import json
from pathlib import Path

STAFF_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "staff.json"))


class StaffData:
    def __init__(self):
        pass

    def load_staff_data(self) -> list[dict]:
        data = []
        with open(STAFF_DATA_PATH, "r") as file:
            read = json.load(file)
            data = read["data"]
        return data

    def is_staff(self, username: str, password: str) -> bool:
        data = self.load_staff_data()
        for info in data:
            if info["name"] == username and info["password"] == password:
                return True
        return False