class Product:
    def __init__(self, product_category, product_type):
        self.product_category = product_category
        self.product_type = product_type

    def description(self):
        return f"{self.product_type} in the {self.product_category} category."


class AudioDevice(Product):
    def __init__(self, product_type):
        super().__init__("Audio Devices", product_type)


class Amplifier(AudioDevice):
    def __init__(self):
        super().__init__("Amplifier")


class Speaker(AudioDevice):
    def __init__(self):
        super().__init__("Speaker")


class Headphone(AudioDevice):
    def __init__(self):
        super().__init__("Headphone")


class Microphone(AudioDevice):
    def __init__(self):
        super().__init__("Microphone")


class VideoDevice(Product):
    def __init__(self, product_type):
        super().__init__("Video Devices", product_type)


class Camera(VideoDevice):
    def __init__(self):
        super().__init__("Camera")


class Machine:
    def __init__(self, machine_id, equipment_type):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced, product):
        if self.is_valid_product(product):
            self.runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product.product_type,
                "product_category": product.product_category
            })
        else:
            raise ValueError(f"Invalid product type '{product.product_type}' for {self.equipment_type}.")

    def is_valid_product(self, product):
        return False

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

    def production_details(self):
        return self.runs

    def __str__(self):
        return f"{self.equipment_type} (ID: {self.machine_id}) - Total Units Produced: {self.total_units_produced()}"


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


class CameraAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Camera Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Camera)


class MicrophoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Microphone Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Microphone)


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


def clean_date(date_str):
    """
    Cleans and parses a date string in YYYY-MM-DD format.

    Args:
        date_str (str): The date string to clean and parse.

    Returns:
        datetime: The parsed datetime object, or None if invalid.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def clean_text(text):
    """
    Cleans and standardizes text by stripping extra spaces and converting to title case.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned and standardized text.
    """
    return text.strip().title()


def read_and_filter_production(file_path, target_date):
    """
    Reads production data from a CSV file and filters machines running on a specific date.

    Args:
        file_path (str): Path to the CSV file.
        target_date (str): The date to filter machines by (in YYYY-MM-DD format).

    Returns:
        dict: A dictionary with machine type as the key and a list of running machines as the value.
    """
    running_machines = {}

    # Parse the target date
    target_date = datetime.strptime(target_date, "%Y-%m-%d")

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse and clean text fields
            equipment_type = clean_text(row["Equipment_Type"])
            product_type = clean_text(row["Product_Type"])

            # Parse dates
            run_start = clean_date(row["Run_Start"])
            run_end = clean_date(row["Run_End"])

            if not run_start or not run_end:
                print(f"Invalid dates for Machine_ID {row['Machine_ID']}. Skipping entry.")
                continue

            # Check if the target date is within the run period
            if run_start <= target_date <= run_end:
                machine_id = row["Machine_ID"]
                units_produced = int(row["Units_Produced"])

                # Validate product and machine types
                if equipment_type not in machine_class_map:
                    print(f"Unknown machine type '{equipment_type}' for Machine_ID {machine_id}. Skipping.")
                    continue

                if product_type not in product_class_map:
                    print(f"Unknown product type '{product_type}' for Machine_ID {machine_id}. Skipping.")
                    continue

                # Initialize or fetch the machine
                machine_class = machine_class_map[equipment_type]
                product_class = product_class_map[product_type]
                product = product_class()

                if equipment_type not in running_machines:
                    running_machines[equipment_type] = []

                machine = next((m for m in running_machines[equipment_type] if m.machine_id == machine_id), None)
                if not machine:
                    machine = machine_class(machine_id)
                    running_machines[equipment_type].append(machine)

                # Add production run
                try:
                    machine.add_run(row["Run_Start"], row["Run_End"], units_produced, product)
                except ValueError as e:
                    print(e)

    return running_machines


def display_running_machines(running_machines):
    """
    Displays running machines grouped by type and ID with production details.

    Args:
        running_machines (dict): Dictionary of machines grouped by type.
    """
    for equipment_type, machines in running_machines.items():
        print(f"\n{equipment_type}:")
        for machine in machines:
            print(f"  {machine}")
            for run in machine.production_details():
                print(f"    Run Start: {run['run_start']}, Run End: {run['run_end']}, Units Produced: {run['units_produced']}, Product Type: {run['product_type']}")


if __name__ == "__main__":
    # File path and target date
    file_path = "Training_Datasets/Day1/production_line_data.csv"
    target_date = "2020-02-26"  # Example target date

    # Read and filter production data
    running_machines = read_and_filter_production(file_path, target_date)

    # Display results
    print(f"Machines running on {target_date}:")
    display_running_machines(running_machines)
