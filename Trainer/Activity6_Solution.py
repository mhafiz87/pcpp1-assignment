class Product:
    def __init__(self, product_category, product_type):
        self._product_category = product_category
        self._product_type = product_type

    @property
    def product_category(self):
        """Getter for product category."""
        return self._product_category

    @product_category.setter
    def product_category(self, value):
        """Setter for product category."""
        if isinstance(value, str) and len(value) > 0:
            self._product_category = value
        else:
            raise ValueError("Product category must be a non-empty string.")

    @property
    def product_type(self):
        """Getter for product type."""
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        """Setter for product type."""
        if isinstance(value, str) and len(value) > 0:
            self._product_type = value
        else:
            raise ValueError("Product type must be a non-empty string.")

    def description(self):
        return f"{self._product_type} in the {self._product_category} category."


# Audio Devices
class AudioDevice(Product):
    def __init__(self, product_type):
        super().__init__("Audio Devices", product_type)


class Speaker(AudioDevice):
    def __init__(self):
        super().__init__("Speaker")


class Headphone(AudioDevice):
    def __init__(self):
        super().__init__("Headphone")


class Amplifier(AudioDevice):
    def __init__(self):
        super().__init__("Amplifier")


class Microphone(AudioDevice):
    def __init__(self):
        super().__init__("Microphone")


# Video Devices
class VideoDevice(Product):
    def __init__(self, product_type):
        super().__init__("Video Devices", product_type)


class Camera(VideoDevice):
    def __init__(self):
        super().__init__("Camera")

class Machine:
    authorized_users = ["machine_operator"]  # Class attribute for role validation

    def __init__(self, machine_id, equipment_type):
        self._machine_id = machine_id
        self._equipment_type = equipment_type
        self._runs = []

    @property
    def machine_id(self):
        """Getter for machine ID."""
        return self._machine_id

    @property
    def equipment_type(self):
        """Getter for equipment type."""
        return self._equipment_type

    @property
    def runs(self):
        """Getter for runs (access restricted to machine operators)."""
        user = getattr(self, "current_user", None)
        if user in self.authorized_users:
            return self._runs
        else:
            raise PermissionError("Access denied. Only machine operators can access runs.")

    def add_run(self, run_start, run_end, units_produced, product):
        if self.is_valid_product(product):
            self._runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product.product_type,
                "product_category": product.product_category,
            })
        else:
            raise ValueError(f"Invalid product type '{product.product_type}' for {self._equipment_type}.")

    def is_valid_product(self, product):
        return False

    @staticmethod
    def is_valid_date(date_str):
        """Static method to validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @classmethod
    def authorize_user(cls, user):
        """Class method to add a new authorized user."""
        if isinstance(user, str):
            cls.authorized_users.append(user)
        else:
            raise ValueError("User must be a string representing the role.")

    def __str__(self):
        return f"{self._equipment_type} (ID: {self._machine_id}) - Total Units Produced: {self.total_units_produced()}"

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self._runs)

    def production_details(self):
        user = getattr(self, "current_user", None)
        if user in self.authorized_users:
            return self._runs
        else:
            raise PermissionError("Access denied. Only machine operators can access production details.")


# Machine Subclasses
class SpeakerAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Speaker Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Speaker)


class HeadphoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Headphone Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Headphone)


class AmplifierAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Amplifier Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Amplifier)


class MicrophoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Microphone Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Microphone)


class CameraAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Camera Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Camera)

class Validator:
    @staticmethod
    def validate_text(text):
        """Validates if a string is non-empty and stripped of unnecessary spaces."""
        if isinstance(text, str) and len(text.strip()) > 0:
            return text.strip()
        else:
            raise ValueError("Invalid text input.")

    @staticmethod
    def validate_positive_integer(value):
        """Validates if a value is a positive integer."""
        if isinstance(value, int) and value > 0:
            return value
        else:
            raise ValueError("Value must be a positive integer.")

import csv
from datetime import datetime

# Mapping machine types to their respective classes
machine_class_map = {
    "Speaker Assembly Machine": SpeakerAssemblyMachine,
    "Headphone Assembly Machine": HeadphoneAssemblyMachine,
    "Amplifier Assembly Machine": AmplifierAssemblyMachine,
    "Camera Assembly Machine": CameraAssemblyMachine,
    "Microphone Assembly Machine": MicrophoneAssemblyMachine,
}

# Mapping product types to their respective classes
product_class_map = {
    "Speakers": Speaker,
    "Headphones": Headphone,
    "Amplifiers": Amplifier,
    "Cameras": Camera,
    "Microphones": Microphone,
}



def read_production_file(file_path, target_date, current_user):
    running_machines = {}

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                equipment_type = Validator.validate_text(row["Equipment_Type"])
                product_type = Validator.validate_text(row["Product_Type"])
                run_start = Validator.validate_text(row["Run_Start"])
                run_end = Validator.validate_text(row["Run_End"])
                units_produced = Validator.validate_positive_integer(int(row["Units_Produced"]))

                if not Machine.is_valid_date(run_start) or not Machine.is_valid_date(run_end):
                    print(f"Invalid dates for Machine_ID {row['Machine_ID']}. Skipping.")
                    continue

                if datetime.strptime(run_start, "%Y-%m-%d") <= datetime.strptime(target_date, "%Y-%m-%d") <= datetime.strptime(run_end, "%Y-%m-%d"):
                    if equipment_type not in running_machines:
                        running_machines[equipment_type] = []

                    product = product_class_map[product_type]()
                    machine_class = machine_class_map[equipment_type]
                    machine = machine_class(row["Machine_ID"])
                    machine.current_user = current_user  # Set the current user

                    machine.add_run(run_start, run_end, units_produced, product)
                    running_machines[equipment_type].append(machine)

            except Exception as e:
                print(f"Error processing row: {e}")

    return running_machines

if __name__ == "__main__":
    file_path = "Training_Datasets/Day1/production_line_data.csv"
    target_date = "2020-02-26"
    current_user = "machine_operator"

    running_machines = read_production_file(file_path, target_date, current_user)
    for equipment_type, machines in running_machines.items():
        print(f"\n{equipment_type}:")
        for machine in machines:
            print(machine)
