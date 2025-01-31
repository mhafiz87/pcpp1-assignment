class TV:
    
    def __init__(self, machine_id, equipment_type, size, resolution, display_type):
        self.machine_id = machine_id
        self.equipment_type = equipment_type
        self.runs = []
        self.size = size
        self.resolution = resolution
        self.display = display_type

    def add_run(self, run_start, run_end, units_produced):
        self.runs.append({
        "run_start": run_start,
        "run_end": run_end,
        "units_produced": units_produced
        })
        
    def total_units_produced(self):

        return sum(run["units_produced"] for run in self.runs)
    
tv_sony = TV("SONY_TV-0001", "TV", "85", "8K", "OLED")
tv_sony.add_run("2024-12-25", "2024-12-31", 500)
tv_sony.add_run("2024-12-25", "2024-12-31", 500)

print(f"Total Units Produced: {tv_sony.total_units_produced()}")