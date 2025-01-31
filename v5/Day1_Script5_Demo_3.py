class Machine:
    def __init__(self, machine_id, equipment_type):
        self.__machine_id = machine_id  # Private attribute
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced):
        if run_end <= run_start:
            raise ValueError("Run_End must be after Run_Start.")
        if units_produced <= 0:
            raise ValueError("Units_Produced must be positive.")
        self.runs.append({"run_start": run_start, "run_end": run_end, "units_produced": units_produced})

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

# Example Usage
if __name__ == "__main__":
    machine = Machine("MC-1001", "Speaker Assembly Machine")
    try:
        machine.add_run("2024-01-01", "2024-01-07", 210)
        machine.add_run("2024-01-10", "2024-01-05", 300)  # Invalid run
    except ValueError as e:
        print(f"Error: {e}")
    print(f"Total Units Produced: {machine.total_units_produced()}")
