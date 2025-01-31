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
    

class Product:
    def __init__(self, product_category, product_type):
        self.product_category = product_category
        self.product_type = product_type
        self.components = []

    def add_components(self, part_name, quantity):
        self.components.append({
            "part_name":part_name,
            "quantity":quantity
        })


# Example Usage
machine = Machine("MC-1001", "Speaker Assembly Machine")
machine.add_run("2024-01-01", "2024-01-07", 210)
machine.add_run("2024-01-10", "2024-01-24", 420)
print(f"Total Units Produced: {machine.total_units_produced()}")