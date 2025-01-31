class Machine:
    def __init__(self, machine_id, equipment_type):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced, product):
        self.runs.append({
            "run_start": run_start,
            "run_end": run_end,
            "units_produced": units_produced,
            "product_category": product.product_category,
            "product_type": product.product_type,
        })

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

# todo Type assembly line


class Product:
    def __init__(self, product_category, product_type):
        self.product_category = product_category
        self.product_type = product_type


class AudioDevices(Product):  # todo class type
    def __init__(self, product_type):
        super().__init__(product_category="Audio Devices", product_type=product_type)

    def functionality(self):
        print("My function: I produce sound!")


class VideoDevices(Product):  # todo class type
    def __init__(self, product_type):
        super().__init__(product_category="Video Devices", product_type=product_type)

    def functionality(self):
        print("My function: I capture picture!")


# Example Usage
microphone = AudioDevices("microphone")
camera = VideoDevices("camera")
microphone.functionality()
camera.functionality()

machine = Machine("MC-1001", "Speaker Assembly Machine")
machine.add_run("2024-01-01", "2024-01-07", 210, microphone)
machine.add_run("2024-01-10", "2024-01-24", 420, camera)

# Print something
