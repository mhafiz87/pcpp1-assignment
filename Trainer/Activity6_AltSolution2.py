# Required standard packages
import csv
from datetime import datetime

class ValidationError(ValueError):
    """Custom exception for validation errors."""
    def __init__(self, message):
        super().__init__(f"Validation Error: {message}")


class PermissionErrorCustom(PermissionError):
    """Custom exception for permission-related errors."""
    def __init__(self, message):
        super().__init__(f"Permission Denied: {message}")


class ProductTypeError(TypeError):
    """Custom exception for invalid product types."""
    def __init__(self, message):
        super().__init__(f"Product Type Error: {message}")

class Product:
    def __init__(self, product_category, product_type):
        self.product_category = product_category
        self.product_type = product_type

    @property
    def product_category(self):
        return self._product_category

    @product_category.setter
    def product_category(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._product_category = value.strip()
        else:
            raise ValidationError("Product category must be a non-empty string.")

    @property
    def product_type(self):
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._product_type = value.strip()
        else:
            raise ValidationError("Product type must be a non-empty string.")

    def description(self):
        return f"{self.product_type} in the {self.product_category} category."


# Subclasses for Audio Devices
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


# Subclasses for Video Devices
class VideoDevice(Product):
    def __init__(self, product_type):
        super().__init__("Video Devices", product_type)


class Camera(VideoDevice):
    def __init__(self):
        super().__init__("Camera")

class Machine:
    authorized_users = ["machine_operator"]  # Authorized roles

    def __init__(self, machine_id, equipment_type):
        self._machine_id = machine_id
        self._equipment_type = equipment_type
        self._runs = []
        self.current_user = None  # To store the current user role

    @property
    def machine_id(self):
        return self._machine_id

    @property
    def equipment_type(self):
        return self._equipment_type

    @property
    def runs(self):
        self.validate_user()  # Validate user before accessing runs
        return self._runs

    def add_run(self, run_start, run_end, units_produced, product):
        self.validate_user()  # Validate user before adding a run
        if self.is_valid_product(product):
            self._runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product.product_type,
                "product_category": product.product_category,
            })
        else:
            raise ProductTypeError(f"Invalid product type '{product.product_type}' for {self._equipment_type}.")

    def is_valid_product(self, product):
        return False

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self._runs)

    def production_details(self):
        self.validate_user()  # Validate user before accessing production details
        return self._runs

    def __str__(self):
        return f"{self._equipment_type} (ID: {self._machine_id}) - Total Units Produced: {self.total_units_produced()}"

    def validate_user(self):
        """
        Validates if the current user is authorized to perform the operation.
        """
        if self.current_user not in self.authorized_users:
            raise PermissionErrorCustom("Access denied. Only authorized users can perform this operation.")


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
        if isinstance(text, str) and len(text.strip()) > 0:
            return text.strip()
        else:
            raise ValidationError("Text input must be a non-empty string.")

    @staticmethod
    def validate_positive_integer(value):
        if isinstance(value, int) and value > 0:
            return value
        else:
            raise ValidationError("Value must be a positive integer.")

    @staticmethod
    def validate_date(date_str):
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid date format. Expected YYYY-MM-DD.")

# Map Machine Types to Machine Classes
machine_class_map = {
    "Speaker Assembly Machine": SpeakerAssemblyMachine,
    "Headphone Assembly Machine": HeadphoneAssemblyMachine,
    "Amplifier Assembly Machine": AmplifierAssemblyMachine,
    "Microphone Assembly Machine": MicrophoneAssemblyMachine,
    "Camera Assembly Machine": CameraAssemblyMachine,
}

# Map Product Types to Product Classes
product_class_map = {
    "Speakers": Speaker,
    "Headphones": Headphone,
    "Amplifiers": Amplifier,
    "Microphones": Microphone,
    "Cameras": Camera,
}

def read_production_file(file_path, target_date, current_user):
    """
    Reads the production file and processes data based on the target date and user role.
    """
    running_machines = {}

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                equipment_type = Validator.validate_text(row["Equipment_Type"])
                product_type = Validator.validate_text(row["Product_Type"])
                run_start = Validator.validate_date(row["Run_Start"])
                run_end = Validator.validate_date(row["Run_End"])
                units_produced = Validator.validate_positive_integer(int(row["Units_Produced"]))

                # Ensure the target date is within the production run period
                if run_start <= datetime.strptime(target_date, "%Y-%m-%d") <= run_end:
                    if equipment_type not in running_machines:
                        running_machines[equipment_type] = []

                    product = product_class_map[product_type]()
                    machine_class = machine_class_map[equipment_type]
                    machine = machine_class(row["Machine_ID"])
                    machine.current_user = current_user  # Set the current user for validation

                    machine.add_run(run_start, run_end, units_produced, product)
                    running_machines[equipment_type].append(machine)

            except ValidationError as ve:
                print(f"Validation error: {ve}")
            except PermissionErrorCustom as pe:
                print(f"Permission error: {pe}")
            except ProductTypeError as pte:
                print(f"Product type error: {pte}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    return running_machines


if __name__ == "__main__":
    file_path = "Training_Datasets/Day1/production_line_data.csv"
    target_date = "2020-02-26"
    current_user = "machine_spoiler"  # Change this to test unauthorized access

    # Validate current user before processing
    if current_user not in Machine.authorized_users:
        print(f"Access denied for user '{current_user}'. Only authorized users can perform this operation.")
    else:
        running_machines = read_production_file(file_path, target_date, current_user)
        for equipment_type, machines in running_machines.items():
            print(f"\n{equipment_type}:")
            for machine in machines:
                print(machine)
