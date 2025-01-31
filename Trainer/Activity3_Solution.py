class Machine:
    def __init__(self, machine_id, equipment_type):
        """
        Initialize a Machine object.

        Args:
            machine_id (str): Unique identifier for the machine.
            equipment_type (str): The type of machine (e.g., "Speaker Assembly Machine").
        """
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced, product_type):
        """
        Adds a production run to the machine.

        Args:
            run_start (str): Start date of the production run.
            run_end (str): End date of the production run.
            units_produced (int): Number of units produced during the run.
            product_type (str): The product type for the production run.

        Returns:
            str: Confirmation message if the product type is valid, otherwise raises an exception.
        """
        if self.is_valid_product(product_type):
            self.runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product_type
            })
            return f"Production run added for {product_type}."
        else:
            raise ValueError(f"Invalid product type '{product_type}' for {self.equipment_type}.")

    def is_valid_product(self, product_type):
        """
        Placeholder for validating product types. Must be overridden by subclasses.

        Args:
            product_type (str): The product type to validate.

        Returns:
            bool: Always False in base class.
        """
        return False

    def total_units_produced(self):
        """
        Calculate the total units produced across all runs.

        Returns:
            int: Total units produced.
        """
        return sum(run["units_produced"] for run in self.runs)

    def production_details(self):
        """
        Get detailed information about all production runs.

        Returns:
            list: A list of dictionaries containing production run details.
        """
        return self.runs

class SpeakerAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Speaker Assembly Machine")

    def is_valid_product(self, product_type):
        return product_type == "Speaker"

class HeadphoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Headphone Assembly Machine")

    def is_valid_product(self, product_type):
        return product_type == "Headphone"

class AmplifierAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Amplifier Assembly Machine")

    def is_valid_product(self, product_type):
        return product_type == "Amplifier"

class CameraAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Camera Assembly Machine")

    def is_valid_product(self, product_type):
        return product_type == "Camera"

class MicrophoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Microphone Assembly Machine")

    def is_valid_product(self, product_type):
        return product_type == "Microphone"

if __name__ == "__main__":
    # Create machines
    speaker_machine = SpeakerAssemblyMachine("MC-1001")
    microphone_machine = MicrophoneAssemblyMachine("MC-1002")

    # Valid production runs
    try:
        print(speaker_machine.add_run("2024-01-01", "2024-01-07", 210, "Speaker"))
        print(microphone_machine.add_run("2024-01-10", "2024-01-20", 420, "Microphone"))
    except ValueError as e:
        print(e)

    # Invalid production run
    try:
        print(microphone_machine.add_run("2024-02-01", "2024-02-10", 300, "Speaker"))
    except ValueError as e:
        print(e)

    # Display total units produced
    print(f"Total units produced by Speaker Machine: {speaker_machine.total_units_produced()}")
    print(f"Total units produced by Microphone Machine: {microphone_machine.total_units_produced()}")

    # Display production details
    print("\nProduction Details for Speaker Machine:")
    for run in speaker_machine.production_details():
        print(run)

    print("\nProduction Details for Microphone Machine:")
    for run in microphone_machine.production_details():
        print(run)
