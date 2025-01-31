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
    def __init__(self, product_category:str, product_type:str):
        self.product_category = product_category
        self.product_type = product_type
        self.components = []

    def add_components(self, part_name, quantity):
        self.components.append({
            "part_name":part_name,
            "quantity":quantity
        })

class Speaker(Product):
    def __init__(self, product_category:str, product_type:str, driver_size:float):
        super().__init__(product_category,product_type)
        self.driver_size = driver_size

    def get_driver_size(self):
        return self.driver_size

class Headphone(Product):
    def __init__(self, product_category:str, product_type:str, type:str):
        super().__init__(product_category,product_type)
        self.type = type

    def get_headphone_type(self):
        return self.type

class Amplifier(Product):
    def __init__(self, product_category:str, product_type:str, amplifier_class:str):
        super().__init__(product_category,product_type)
        self.amplifier_class = amplifier_class

    def get_amplifier_class(self):
        return self.amplifier_class

class Camera(Product):
    def __init__(self, product_category:str, product_type:str, type:str):
        super().__init__(product_category,product_type)
        self.type = type

    def get_camera_type(self):
        return self.type

class Microphone(Product):
    def __init__(self, product_category:str, product_type:str, phantom_power:bool):
        super().__init__(product_category,product_type)
        self.phantom_power = phantom_power

    def is_phantom_power(self):
        return self.phantom_power
    

class AssemblySpeaker(Machine):
    def __init__(self, machine_id, equipment_type):
        super().__init__(machine_id, equipment_type)

    def add_run(self, run_start, run_end, units_produced, product:Speaker):
        assert product.__class__.__name__ == "Speaker", f"Product is not Speaker, received: {product.__class__.__name__}"
        return super().add_run(run_start, run_end, units_produced, product)
        
class AssemblyHeadphone(Machine):
    def __init__(self, machine_id, equipment_type):
        super().__init__(machine_id, equipment_type)

    def add_run(self, run_start, run_end, units_produced, product:Headphone):
        assert product.__class__.__name__ == "Headphone", f"Product is not Headphone, received: {product.__class__.__name__}"
        return super().add_run(run_start, run_end, units_produced, product)
        
class AssemblyAmplifier(Machine):
    def __init__(self, machine_id, equipment_type):
        super().__init__(machine_id, equipment_type)

    def add_run(self, run_start, run_end, units_produced, product:Amplifier):
        assert product.__class__.__name__ == "Amplifier", f"Product is not Amplifier, received: {product.__class__.__name__}"
        return super().add_run(run_start, run_end, units_produced, product)
        
class AssemblyMicrophone(Machine):
    def __init__(self, machine_id, equipment_type):
        super().__init__(machine_id, equipment_type)

    def add_run(self, run_start, run_end, units_produced, product:Microphone):
        assert product.__class__.__name__ == "Microphone", f"Product is not Microphone, received: {product.__class__.__name__}"
        return super().add_run(run_start, run_end, units_produced, product)
        

class AssemblyCamera(Machine):
    def __init__(self, machine_id, equipment_type):
        super().__init__(machine_id, equipment_type)

    def add_run(self, run_start, run_end, units_produced, product:Camera):
        assert product.__class__.__name__ == "Camera", f"Product is not Camera, received: {product.__class__.__name__}"
        return super().add_run(run_start, run_end, units_produced, product)
        
if __name__ == "__main__":
    camera_prod = Camera("Video","Camera","DSLR")
    headphone_prod = Headphone("Audio","Headphone","Closed back")
    camera_assem = AssemblyCamera("123","Camera Assembly Machine")
    camera_assem.add_run("09/12/24","10/12/24",300,camera_prod)
    # camera_assem.add_run("09/12/24","10/12/24",300,headphone_prod)
    assert camera_assem.total_units_produced() == 300

