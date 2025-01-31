import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
from user import User
import os

# Setting the directory for user_profile.json, can change if needed
new_directory = "C:/Users/5004122356/Desktop/Downloads"
os.chdir(new_directory)

class DataDialog(simpledialog.Dialog):

    def body(self, master):
        self.text = "Update values: "
        tk.Label(master, text=self.text).grid(row=0,columnspan=2)
        tk.Label(master, text="machine id").grid(row=1,column=0)
        tk.Label(master, text="machine type").grid(row=2,column=0)
        tk.Label(master, text="batch id").grid(row=3,column=0)
        tk.Label(master, text="product type").grid(row=4,column=0)
        tk.Label(master, text="start date").grid(row=5,column=0)
        tk.Label(master, text="end date").grid(row=6,column=0)
        tk.Label(master, text="result").grid(row=7,column=0)
        tk.Label(master, text="remarks").grid(row=8,column=0)
        self.machine_id_var = tk.StringVar()
        self.machine_type_var = tk.StringVar()
        self.batch_id_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.remarks_var = tk.StringVar()
        self.machine_id = tk.Entry(master,width=23,textvariable=self.machine_id_var).grid(row=1,column=1)
        self.machine_type = ttk.Combobox(master,textvariable=self.machine_type_var,state="readonly",width=20).grid(row=2,column=1)
        self.batch_id = tk.Entry(master,width=23,textvariable=self.batch_id_var).grid(row=3,column=1)
        self.product_type = ttk.Combobox(master,textvariable=self.product_var,state="readonly",width=20).grid(row=4,column=1)
        self.start_date = tk.Entry(master,width=23,textvariable=self.start_date_var).grid(row=5,column=1)
        self.end_date = tk.Entry(master,width=23,textvariable=self.end_date_var).grid(row=6,column=1)
        self.result = ttk.Combobox(master,values=["Pass","Fail"],textvariable=self.result_var,state="readonly",width=20).grid(row=7,column=1)
        self.remarks = tk.Entry(master,width=23,textvariable=self.remarks_var).grid(row=8,column=1)

    def apply(self):
        self.result = {
            "machine_id":self.machine_id_var.get(),
            "machine_type":self.machine_type_var.get(),
            "batch_id":self.batch_id_var.get(),
            "product_type":self.product_var.get(),
            "start_date":self.start_date_var.get(),
            "end_date":self.end_date_var.get(),
            "result":self.result_var.get(),
            "remarks":self.remarks_var.get()
        }


class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
        self.geometry("800x600")
        self.current_user = None
        self.running_machines = {}
        self.user_data = self.load_user_data("user_profile.json")  # Load JSON file
        self.data_has_been_modified = False

        self.create_login_screen()

    def load_user_data(self, json_path):
        """
        Load user data from a JSON file.
        """
        try:
            with open(json_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", f"The JSON file '{json_path}' does not exist.")
            self.quit()  # Exit the application if the file is missing
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"The JSON file '{json_path}' is not properly formatted.")
            self.quit()
        return []


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

        # ttk.Label(self.login_frame, text="Select Role:").pack(pady=5)
        # #TODO: Import list of users
        # self.role_combobox = ttk.Combobox(self.login_frame, values=["machine_operator","product_inspector"], state="readonly")
        # self.role_combobox.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).pack(pady=20)

    def get_user_from_database(self, username):
        """
        Retrieve the user data for a given username from the JSON database.
        """
        for user in self.user_data:
            if user["name"].strip().lower() == username.lower():  # Match username case-insensitively
                return user
        return None

    def handle_login(self):
        """
        Handle login validation.
        """
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        try:
            user_data = self.get_user_from_database(username)  # Validate user
            if not user_data:
                messagebox.showerror("Error", "User not found in the database.")
                return

            # Instantiate the User class
            self.current_user = User(name=username, role=user_data["role"])

            # Proceed to main dashboard
            self.login_frame.destroy()
            self.create_main_dashboard()

        except Exception as e:
            messagebox.showerror("Error", str(e))

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
        self.production_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def return_to_login(self):
        logout = messagebox.askyesno(title="Confirm logout?",message="Are you sure you want to logout? All unsaved data will be lost")
        if logout:
            self.tab_control.destroy()
            self.create_login_screen()

    def on_tree_select(self, event):
        selected_item = self.production_tree.selection()
        if selected_item:
            self.edit_data_button.config(state=tk.NORMAL)
        else:
            self.edit_data_button.config(state=tk.DISABLED)


    def setup_production_tab(self):
        """
        Setup the production data tab.
        """
        ttk.Label(self.production_tab, text="Production Data", font=("Arial", 16)).pack(side="top")
        self.logout_frame = tk.Frame(self.production_tab)
        self.logout_button = ttk.Button(self.logout_frame, text="logout", command=self.return_to_login).pack(side="right")
        self.logout_frame.pack(fill="x",side="top")
        self.button_frame = tk.Frame(self.production_tab)
        self.add_data_button = ttk.Button(self.production_tab, text="add", command=self.add_data).pack(side="right",in_=self.button_frame)
        self.edit_data_button = ttk.Button(self.production_tab, text="edit", command=self.edit_data, state=tk.DISABLED).pack(side="right",in_=self.button_frame)
        self.save_data_button = ttk.Button(self.production_tab, text="save", command=self.filter_data, state=tk.DISABLED).pack(side="right",in_=self.button_frame)
        self.filter_data_button = ttk.Button(self.production_tab, text="filter", command=self.filter_data, state=tk.DISABLED).pack(side="right",in_=self.button_frame)
        self.button_frame.pack(side="top",fill="x",in_=self.production_tab)

        self.tree_frame = tk.Frame(self.production_tab)
        self.data_scrollbar = tk.Scrollbar(self.tree_frame)
        self.data_scrollbar.pack(
            in_=self.tree_frame, side=tk.RIGHT, fill=tk.Y
        )
        self.production_tree = ttk.Treeview(self.production_tab, columns=("Machine ID", "Equipment Type", "Units Produced"),
                                            show="headings",yscrollcommand=self.data_scrollbar.set)
        self.production_tree.heading("Machine ID", text="Machine ID")
        self.production_tree.heading("Equipment Type", text="Equipment Type")
        self.production_tree.heading("Units Produced", text="Units Produced")
        self.production_tree.pack(fill="both", expand=True, in_=self.tree_frame)
        self.data_scrollbar.config(command=self.production_tree.yview)
        # self.load_production_data()
        self.tree_frame.pack(side="top",fill="both", expand=True,in_=self.production_tab)

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

    def edit_data(self):
        mock_data = {}
        pass

    def add_data(self):
        dialog = DataDialog(self)
        print(dialog.result)

    def save_data(self):
        pass

    def filter_data(self):
        pass



if __name__ == "__main__":
    app = ProductionMonitoringApp()
    app.mainloop()
