import csv
from pathlib import Path

CAR_DATA_PATH = Path(__file__).parents[2].joinpath("data", "car.csv")


class CarData:
    def __init__(self):
        pass

    def load_car_data(self) -> dict:
        data = []
        header = []
        with open(CAR_DATA_PATH, "r") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                else:
                    data.append(dict(map(lambda x, y: (x, y), header, row)))
        return data


car_data = CarData()

if __name__ == "__main__":
    car_data = CarData()
    print(car_data.load_car_data())
