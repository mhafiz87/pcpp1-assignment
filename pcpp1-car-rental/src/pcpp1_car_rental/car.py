from pathlib import Path

data_path = Path(__file__).parents[2].joinpath("data", "car.csv")
print(str(data_path))


class CarData:
    def __init__(self):
        pass

    def load_car_data(self) -> dict:
        data = {}
        return data