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
        super.__init__(product_category,product_type)
        self.driver_size = driver_size

    def get_driver_size(self):
        return self.driver_size

class Headphone(Product):
    def __init__(self, product_category:str, product_type:str, type:str):
        super.__init__(product_category,product_type)
        self.type = type

    def get_headphone_type(self):
        return self.type

class Amplifier(Product):
    def __init__(self, product_category:str, product_type:str, amplifier_class:str):
        super.__init__(product_category,product_type)
        self.amplifier_class = amplifier_class

    def get_amplifier_class(self):
        return self.amplifier_class

class Camera(Product):
    def __init__(self, product_category:str, product_type:str, type:str):
        super.__init__(product_category,product_type)
        self.type = type

    def get_camera_type(self):
        return self.type

class Microphone(Product):
    def __init__(self, product_category:str, product_type:str, phantom_power:bool):
        super.__init__(product_category,product_type)
        self.phantom_power = phantom_power

    def is_phantom_power(self):
        return self.phantom_power