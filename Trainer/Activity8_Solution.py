import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime
class ValidationError(ValueError):
    """Custom exception for validation errors."""
    def __init__(self, message):
        super().__init__(f"Validation Error: {message}")


class PermissionErrorCustom(PermissionError):
    """Custom exception for permission-related errors."""
    def __init__(self, message):
        super().__init__(f"Permission Denied: {message}")


class ProductTypeError(TypeError):
    """Custom exception for invalid product types."""
    def __init__(self, message):
        super().__init__(f"Product Type Error: {message}")

class Product:
    def __init__(self, product_category, product_type):
        self.product_category = product_category
        self.product_type = product_type

    @property
    def product_category(self):
        return self._product_category

    @product_category.setter
    def product_category(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._product_category = value.strip()
        else:
            raise ValidationError("Product category must be a non-empty string.")

    @property
    def product_type(self):
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._product_type = value.strip()
        else:
            raise ValidationError("Product type must be a non-empty string.")

    def description(self):
        return f"{self.product_type} in the {self.product_category} category."


# Subclasses for Audio Devices
class AudioDevice(Product):
    def __init__(self, product_type):
        super().__init__("Audio Devices", product_type)


class Speaker(AudioDevice):
    def __init__(self):
        super().__init__("Speaker")


class Headphone(AudioDevice):
    def __init__(self):
        super().__init__("Headphone")


class Amplifier(AudioDevice):
    def __init__(self):
        super().__init__("Amplifier")


class Microphone(AudioDevice):
    def __init__(self):
        super().__init__("Microphone")


# Subclasses for Video Devices
class VideoDevice(Product):
    def __init__(self, product_type):
        super().__init__("Video Devices", product_type)


class Camera(VideoDevice):
    def __init__(self):
        super().__init__("Camera")

class Machine:
    authorized_users = ["machine_operator"]  # Authorized roles

    def __init__(self, machine_id, equipment_type):
        self._machine_id = machine_id
        self._equipment_type = equipment_type
        self._runs = []
        self.current_user = None  # To store the current user role

    @property
    def machine_id(self):
        return self._machine_id

    @property
    def equipment_type(self):
        return self._equipment_type

    @property
    def runs(self):
        self.validate_user()  # Validate user before accessing runs
        return self._runs

    def add_run(self, run_start, run_end, units_produced, product):
        self.validate_user()  # Validate user before adding a run
        if self.is_valid_product(product):
            self._runs.append({
                "run_start": run_start,
                "run_end": run_end,
                "units_produced": units_produced,
                "product_type": product.product_type,
                "product_category": product.product_category,
            })
        else:
            raise ProductTypeError(f"Invalid product type '{product.product_type}' for {self._equipment_type}.")

    def is_valid_product(self, product):
        return False

    def total_units_produced(self):
        return sum(run["units_produced"] for run in self._runs)

    def production_details(self):
        self.validate_user()  # Validate user before accessing production details
        return self._runs

    def __str__(self):
        return f"{self._equipment_type} (ID: {self._machine_id}) - Total Units Produced: {self.total_units_produced()}"

    def validate_user(self):
        """
        Validates if the current user is authorized to perform the operation.
        """
        if self.current_user not in self.authorized_users:
            raise PermissionErrorCustom("Access denied. Only authorized users can perform this operation.")


# Machine Subclasses
class SpeakerAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Speaker Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Speaker)


class HeadphoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Headphone Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Headphone)


class AmplifierAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Amplifier Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Amplifier)


class MicrophoneAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Microphone Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Microphone)


class CameraAssemblyMachine(Machine):
    def __init__(self, machine_id):
        super().__init__(machine_id, "Camera Assembly Machine")

    def is_valid_product(self, product):
        return isinstance(product, Camera)


class Validator:
    @staticmethod
    def validate_text(text):
        if isinstance(text, str) and len(text.strip()) > 0:
            return text.strip()
        else:
            raise ValidationError("Text input must be a non-empty string.")

    @staticmethod
    def validate_positive_integer(value):
        if isinstance(value, int) and value > 0:
            return value
        else:
            raise ValidationError("Value must be a positive integer.")

    @staticmethod
    def validate_date(date_str):
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid date format. Expected YYYY-MM-DD.")

# Map Machine Types to Machine Classes
machine_class_map = {
    "Speaker Assembly Machine": SpeakerAssemblyMachine,
    "Headphone Assembly Machine": HeadphoneAssemblyMachine,
    "Amplifier Assembly Machine": AmplifierAssemblyMachine,
    "Microphone Assembly Machine": MicrophoneAssemblyMachine,
    "Camera Assembly Machine": CameraAssemblyMachine,
}

# Map Product Types to Product Classes
product_class_map = {
    "Speakers": Speaker,
    "Headphones": Headphone,
    "Amplifiers": Amplifier,
    "Microphones": Microphone,
    "Cameras": Camera,
}

def read_production_file(file_path, target_date, current_user):
    """
    Reads the production file and processes data based on the target date and user role.
    """
    running_machines = {}

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                equipment_type = Validator.validate_text(row["Equipment_Type"])
                product_type = Validator.validate_text(row["Product_Type"])
                run_start = Validator.validate_date(row["Run_Start"])
                run_end = Validator.validate_date(row["Run_End"])
                units_produced = Validator.validate_positive_integer(int(row["Units_Produced"]))

                # Ensure the target date is within the production run period
                if run_start <= datetime.strptime(target_date, "%Y-%m-%d") <= run_end:
                    if equipment_type not in running_machines:
                        running_machines[equipment_type] = []

                    product = product_class_map[product_type]()
                    machine_class = machine_class_map[equipment_type]
                    machine = machine_class(row["Machine_ID"])
                    machine.current_user = current_user  # Set the current user for validation

                    machine.add_run(run_start, run_end, units_produced, product)
                    running_machines[equipment_type].append(machine)

            except ValidationError as ve:
                print(f"Validation error: {ve}")
            except PermissionErrorCustom as pe:
                print(f"Permission error: {pe}")
            except ProductTypeError as pte:
                print(f"Product type error: {pte}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    return running_machines

# Base script components from the provided script
# Include Validator, Machine, Product, and custom exception classes here
# (Omitted for brevity but assumed imported as part of the program)

# GUI Application
class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
        self.geometry("800x600")
        self.current_user = None
        self.running_machines = {}

        self.create_login_screen()

    def create_login_screen(self):
        """
        Create the login screen for role-based access control.
        """
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(fill="both", expand=True)

        ttk.Label(self.login_frame, text="Login", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.login_frame, text="Enter Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(self.login_frame, text="Select Role:").pack(pady=5)
        self.role_combobox = ttk.Combobox(self.login_frame, values=["machine_operator"], state="readonly")
        self.role_combobox.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).pack(pady=20)

    def handle_login(self):
        """
        Handle login validation.
        """
        username = self.username_entry.get().strip()
        role = self.role_combobox.get().strip()

        if not username or not role:
            messagebox.showerror("Error", "Please enter a username and select a role.")
            return

        if role not in Machine.authorized_users:
            messagebox.showerror("Access Denied", "You do not have access to this application.")
            return

        self.current_user = role
        self.login_frame.destroy()
        self.create_main_dashboard()

    def create_main_dashboard(self):
        """
        Create the main dashboard after successful login.
        """
        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.production_tab = ttk.Frame(self.tab_control)
        self.error_log_tab = ttk.Frame(self.tab_control)
        self.report_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.production_tab, text="Production Data")
        self.tab_control.add(self.error_log_tab, text="Error Logs")
        self.tab_control.add(self.report_tab, text="Reports")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_production_tab()
        self.setup_error_log_tab()
        self.setup_report_tab()

    def setup_production_tab(self):
        """
        Setup the production data tab.
        """
        ttk.Label(self.production_tab, text="Production Data", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.production_tab, text="Load Production Data", command=self.load_production_data).pack(pady=5)
        self.production_tree = ttk.Treeview(self.production_tab, columns=("Machine ID", "Equipment Type", "Units Produced"),
                                            show="headings")
        self.production_tree.heading("Machine ID", text="Machine ID")
        self.production_tree.heading("Equipment Type", text="Equipment Type")
        self.production_tree.heading("Units Produced", text="Units Produced")
        self.production_tree.pack(fill="both", expand=True, pady=10)

    def setup_error_log_tab(self):
        """
        Setup the error log tab.
        """
        ttk.Label(self.error_log_tab, text="Error Logs", font=("Arial", 16)).pack(pady=10)
        self.error_text = tk.Text(self.error_log_tab, wrap="word")
        self.error_text.pack(fill="both", expand=True, pady=10)

    def setup_report_tab(self):
        """
        Setup the reports tab.
        """
        ttk.Label(self.report_tab, text="Reports", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.report_tab, text="Generate Summary Report", command=self.generate_report).pack(pady=5)
        self.report_text = tk.Text(self.report_tab, wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)

    def load_production_data(self):
        """
        Load production data from a CSV file.
        """
        file_path = filedialog.askopenfilename(title="Select Production Data File", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            self.running_machines = read_production_file(file_path, "2020-02-26", self.current_user)
            self.populate_production_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def populate_production_data(self):
        """
        Populate the production data treeview.
        """
        self.production_tree.delete(*self.production_tree.get_children())
        for equipment_type, machines in self.running_machines.items():
            for machine in machines:
                self.production_tree.insert("", "end", values=(machine.machine_id, machine.equipment_type,
                                                               machine.total_units_produced()))

    def generate_report(self):
        """
        Generate a summary report.
        """
        self.report_text.delete(1.0, tk.END)
        if not self.running_machines:
            self.report_text.insert(tk.END, "No data available to generate a report.")
            return

        report_lines = []
        for equipment_type, machines in self.running_machines.items():
            report_lines.append(f"Equipment Type: {equipment_type}")
            for machine in machines:
                report_lines.append(f"  {machine.machine_id}: {machine.total_units_produced()} units produced")
            report_lines.append("")

        self.report_text.insert(tk.END, "\n".join(report_lines))


if __name__ == "__main__":
    app = ProductionMonitoringApp()
    app.mainloop()
