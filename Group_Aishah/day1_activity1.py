class Machine:
    def __init__(self, machine_id, equipment_type, product_catergory="", product_type=""):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.product_catergory = product_catergory
        self.product_type = product_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced, product):
        # assume product's category is same to machine category's product_catergory, its 1 to 1 relationship
        # product_id and serial_no to be include when init product
        # assume the value of units_producted is the number of product
        self.runs.append({
            "run_start": run_start,
            "run_end": run_end,
            "units_produced": units_produced,
            "type": product.type,
            "color": product.color,
            "model": product.model
        })

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

class Product:
    def __init__(self, 
        # product_id, 
        category, type, color, model,
        # serial_no
    ) -> None:
        # self.product_id = product_id
        self.category = category # audio / visual
        self.type = type # speaker / headphone / amplifier / camera / microphone
        self.color = color
        self.model = model
        # self.serial_no = serial_no

    def turn_on(self):
        print("turn on product")

    def turn_off(self):
        print("turn off product")


class Speakers(Product):
    def turn_on(self):
        print("turn on speakers")

    def turn_off(self):
        print("turn off speakers")


class Camera(Product):
    def turn_on(self):
        print("turn on camera")

    def turn_off(self):
        print("turn off camera")

class SpeakersBluetooth(Speakers):
    def turn_on(self):
        print("turn on bluetooth speakers")

    def turn_off(self):
        print("turn off bluetooth speakers")

    def connect_bluetooth(self):
        print("successfully connected to bluetooth")


# Example Usage
machine = Machine("MC-1001", "Speaker Assembly Machine")
# machine.add_run("2024-01-01", "2024-01-07", 210)
# machine.add_run("2024-01-10", "2024-01-24", 420)

print(f"Total Units Produced: {machine.total_units_produced()}")

machine_5673 = Machine("MC-5673", "Speaker Assembly Machine", "Audio Devices", "Speakers")
product = Product("audio", "speaker", "black", "sony")
machine_5673.add_run("2024-01-10", "2024-01-24", 420, product)

product_list = [
    Speakers("audio", "speaker", "black", "sony"),
    SpeakersBluetooth("audio", "speaker", "black", "sony"),
    Camera("visual", "camera", "black", "sony"),
]

for product in product_list:
    product.turn_on()