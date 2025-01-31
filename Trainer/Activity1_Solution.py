class Product:
    def __init__(self, product_category, product_type):
        """
        Initialize a Product object.

        Args:
            product_category (str): The category of the product (e.g., "Audio Devices").
            product_type (str): The specific type of product (e.g., "Speakers").
        """
        self.product_category = product_category
        self.product_type = product_type

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
            product (Product): Product details associated with the run.
        """
        self.runs.append({
            "run_start": run_start,
            "run_end": run_end,
            "units_produced": units_produced,
            "product_category": product.product_category,
            "product_type": product.product_type
        })

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

if __name__ == "__main__":
    # Create Product instances
    product1 = Product("Audio Devices", "Speakers")
    product2 = Product("Audio Devices", "Headphones")

    # Create Machine instances
    machine1 = Machine("MC-5673", "Speaker Assembly Machine")
    machine2 = Machine("MC-4904", "Headphone Assembly Machine")

    # Add production runs to machines
    machine1.add_run("12/2/2020", "26/2/2020", 420, product1)
    machine2.add_run("8/10/2020", "29/10/2020", 420, product2)
    machine1.add_run("14/7/2020", "4/8/2020", 630, product1)

    # Display total units produced for each machine
    print(f"Machine {machine1.machine_id} produced a total of {machine1.total_units_produced()} units.")
    print(f"Machine {machine2.machine_id} produced a total of {machine2.total_units_produced()} units.")

    # Display production details for each machine
    print("\nProduction Details for Machine 1:")
    for run in machine1.production_details():
        print(run)

    print("\nProduction Details for Machine 2:")
    for run in machine2.production_details():
        print(run)
