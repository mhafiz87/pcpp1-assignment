import csv

class Machine:
    def __init__(self, machine_id, equipment_type):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []

    def add_run(self, run_start, run_end, units_produced):
        self.runs.append({
            "run_start": run_start,
            "run_end": run_end,
            "units_produced": units_produced
        })

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self.runs)

if __name__ == "__main__":
    machines = {}

    # Load data from CSV
    with open("Training_Datasets/Day1/production_line_data.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            machine_id = row["Machine_ID"]
            if machine_id not in machines:
                machines[machine_id] = Machine(machine_id, row["Equipment_Type"])
            machines[machine_id].add_run(row["Run_Start"], row["Run_End"], int(row["Units_Produced"]))

    # Display total production
    for machine_id, machine in machines.items():
        print(f"Machine {machine_id} produced {machine.total_units_produced()} units.")
