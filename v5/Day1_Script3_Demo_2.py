class Machine:
    all_machines = []

    def __init__(self, machine_id, equipment_type):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []
        Machine.all_machines.append(self)

    def add_run(self, run_start, run_end, units_produced):
        self.runs.append({
            "run_start": run_start,
            "run_end": run_end,
            "units_produced": units_produced
        })

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

    @staticmethod
    def total_production():
        return sum(machine.total_units_produced() for machine in Machine.all_machines)

# Example Usage
if __name__ == "__main__":
    machine1 = Machine("MC-1001", "Speaker Assembly Machine")
    machine1.add_run("2024-01-01", "2024-01-07", 210)

    machine2 = Machine("MC-1002", "Camera Assembly Machine")
    machine2.add_run("2024-02-01", "2024-02-14", 140)

    print(f"Total Production: {Machine.total_production()}")
