class Product:
    def __init__(self, product_category, product_type):
        """
        Initialize a Product object.

        Args:
            product_category (str): Category of the product (e.g., "Audio Devices").
            product_type (str): Specific type of product (e.g., "Amplifier").
        """
        self.product_category = product_category
        self.product_type = product_type

    def description(self):
        """
        Placeholder method for specific product descriptions.
        Should be overridden by subclasses.

        Returns:
            str: A generic description of the product.
        """
        return f"A generic {self.product_type} in the {self.product_category} category."

class AudioDevice(Product):
    def __init__(self, product_type):
        super().__init__("Audio Devices", product_type)

class Amplifier(AudioDevice):
    def __init__(self):
        super().__init__("Amplifier")

    def description(self):
        return "An Amplifier that enhances audio signals for high-quality output."

class Speaker(AudioDevice):
    def __init__(self):
        super().__init__("Speaker")

    def description(self):
        return "A Speaker that produces sound from audio signals."

class VideoDevice(Product):
    def __init__(self, product_type):
        super().__init__("Video Devices", product_type)

class Camera(VideoDevice):
    def __init__(self):
        super().__init__("Camera")

    def description(self):
        return "A Camera that captures high-definition video and images."

class Machine:
    def __init__(self, machine_id, equipment_type):
        """
        Initialize a Machine object.

        Args:
            machine_id (str): Unique identifier for the machine.
            equipment_type (str): Type of the machine (e.g., "Speaker Assembly Machine").
        """
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced, product):
        """
        Adds a production run to the machine.

        Args:
            run_start (str): Start date of the production run.
            run_end (str): End date of the production run.
            units_produced (int): Number of units produced during the run.
            product (Product): The product being produced.

        Raises:
            ValueError: If the product type is invalid for the machine.
        """
        if self.is_valid_product(product):
            self.runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product.product_type,
                "product_category": product.product_category
            })
        else:
            raise ValueError(f"{self.equipment_type} cannot produce {product.product_type}.")

    def is_valid_product(self, product):
        """
        Placeholder for validating products. Should be overridden by subclasses.

        Args:
            product (Product): The product to validate.

        Returns:
            bool: Always False in the base class.
        """
        return False

    def total_units_produced(self):
        """
        Calculate the total units produced.

        Returns:
            int: Total units produced.
        """
        return sum(run["units_produced"] for run in self.runs)

class SpeakerAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Speaker Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Speaker)

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

if __name__ == "__main__":
    # Create products
    speaker = Speaker()
    amplifier = Amplifier()
    camera = Camera()

    # Create machines
    speaker_machine = SpeakerAssemblyMachine("MC-1001")
    amplifier_machine = AmplifierAssemblyMachine("MC-1002")
    camera_machine = CameraAssemblyMachine("MC-1003")

    # Valid runs
    try:
        speaker_machine.add_run("2024-01-01", "2024-01-10", 300, speaker)
        amplifier_machine.add_run("2024-01-15", "2024-01-20", 150, amplifier)
        print("Valid runs added successfully!")
    except ValueError as e:
        print(e)

    # Invalid run
    try:
        camera_machine.add_run("2024-01-25", "2024-01-30", 200, speaker)
    except ValueError as e:
        print(e)

    # Display total production
    print(f"Total units produced by Speaker Machine: {speaker_machine.total_units_produced()}")
    print(f"Total units produced by Amplifier Machine: {amplifier_machine.total_units_produced()}")

    # Production details
    print("\nProduction details for Speaker Machine:")
    for run in speaker_machine.runs:
        print(run)
