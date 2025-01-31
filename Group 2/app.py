import csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from data import ProductionData
from user import User
import logging
from datetime import datetime
import atexit


logging.basicConfig(
    filename="user_interaction.log",
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def log_app_closed():
    logging.info("App has been closed via X button")
atexit.register(log_app_closed)

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prod_data, ui_data, permission_data, combobox_data):
        self.prod_data = prod_data
        self.ui_data = ui_data
        self.permission_data = permission_data
        self.combobox_data = combobox_data
        super().__init__(parent, title)

    def body(self, master):
        self.entries = {}
        row = 0
        for key, value in self.prod_data.items():
            ui = self.ui_data.get(key,"entry")
            tk.Label(master, text=key).grid(row=row, column=0, padx=5, pady=5)
            if ui == "entry":
                entry = tk.Entry(master,width=33)
                entry.grid(row=row, column=1, padx=5, pady=5)
                entry.insert(0, value)
                entry.config(state=self.permission_data[key])
                self.entries[key] = entry
            elif ui =="combobox":
                entry = ttk.Combobox(master,state=self.permission_data[key],width=30,values=self.combobox_data.get(key,[]))
                entry.set(value)
                entry.grid(row=row, column=1, padx=5, pady=5)
                if key == "machine_type":
                    entry.bind("<<ComboboxSelected>>",self.update_product_type)
                self.entries[key] = entry

            row += 1
        return list(self.entries.values())[0]  # initial focus
    
    def update_product_type(self, master):
        self.entries["product_type"].config(state="normal")
        self.entries["product_type"].delete(0,tk.END)
        self.entries["product_type"].insert(0,self.entries["machine_type"].get().split(" ")[0])
        self.entries["product_type"].config(state="readonly")


    def apply(self):
        self.result = {key: entry.get() for key, entry in self.entries.items()}

class FilterDialog(simpledialog.Dialog):
    def __init__(self, parent, title, filter_options, production_data):
        self.filter_options = filter_options
        self.production_data = production_data
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Choose your filter options").grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.options_box = ttk.Combobox(master,width=20,values=self.filter_options,state="readonly")
        self.options_box.grid(row=1,column=0, padx=5, pady=5)
        self.value_box = ttk.Combobox(master,width=20,values=self.filter_options,state="readonly")
        self.value_box.grid(row=1,column=1, padx=5, pady=5)
        self.options_box.bind("<<ComboboxSelected>>",self.get_options)

    def get_options(self, master):
        self.value_box.config(state="normal")
        self.value_box.delete(0,tk.END)
        self.value_box.config(values=self.production_data.get_column_values(self.options_box.get()))
        self.value_box.config(state="readonly")

    def apply(self):
        self.result = (self.options_box.get(), self.value_box.get())
        


class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
        self.geometry("800x600")
        self.current_user = None
        self.jobs = {}
        self.production_data = ProductionData()
        # self.user = User()
        self.prod_data = {'machine_id': '', 'machine_type': '', 'batch_id': '', 'product_type': '', 'start_date': '', 'end_date': '', 'units': '', 'result': '', 'remarks': ''}
        self.ui_data =  {'machine_id': 'entry', 'machine_type': 'combobox', 'batch_id': 'entry', 'product_type': 'entry', 'start_date': 'entry', 'end_date': 'entry', 'units': 'entry', 'result': 'combobox', 'remarks': 'entry'}
        self.permission_data =  {'machine_id': 'normal', 'machine_type': 'normal', 'batch_id': 'normal', 'product_type': 'readonly', 'start_date': 'normal', 'end_date': 'normal', 'units': 'normal', 'result': 'normal', 'remarks': 'normal'}
        self.product_list = self.production_data.product_list
        self.machine_list = self.production_data.machine_list
        self.result_list = ["pass","fail"]
        self.combobox_data = {"machine_type":self.machine_list,"product_type":self.product_list,"result":self.result_list}

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

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).pack(pady=20)

    def handle_login(self):
        """
        Handle login validation.
        """
        username = self.username_entry.get().strip()
        if not User.is_user_in_database(username):
            messagebox.showerror("User not found",f"Invalid user: {username}")
            return
        self.user = User(username)
        logging.info(f"Logged in as {self.user.name} who is a(n) {self.user.role}")
        self.login_frame.destroy()
        self.create_main_dashboard()
        self.set_user_permissions()

    def create_main_dashboard(self):
        """
        Create the main dashboard after successful login.
        """
        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.production_tab = ttk.Frame(self.tab_control)
        self.log_tab = ttk.Frame(self.tab_control)
        self.report_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.production_tab, text="Production Data")
        self.tab_control.add(self.log_tab, text="Logs")
        self.tab_control.add(self.report_tab, text="Reports")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_report_tab()
        self.setup_log_tab()
        self.setup_production_tab()
        self.production_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def return_to_login(self):
        logout = messagebox.askyesno(title="Confirm logout?",message="Are you sure you want to logout? We will miss you :(")
        if logout:
            self.tab_control.destroy()
            logging.info(f"Logged out of user: {self.user.name}")
            self.create_login_screen()


    def setup_production_tab(self):
        """
        Setup the production data tab.
        """
        ttk.Label(self.production_tab, text="Production Data", font=("Arial", 16)).pack(side="top")
        self.logout_frame = tk.Frame(self.production_tab)
        self.logout_button = ttk.Button(self.logout_frame, text="logout", command=self.return_to_login).pack(side="right",padx=5)
        self.logout_frame.pack(fill="x",side="top",pady=20)
        self.button_frame = tk.Frame(self.production_tab)
        self.add_data_button = ttk.Button(self.production_tab, text="add", command=self.add_data)
        self.add_data_button.pack(side="right",in_=self.button_frame,padx=5)
        self.edit_data_button = ttk.Button(self.production_tab, text="edit", command=self.edit_data, state=tk.DISABLED)
        self.edit_data_button.pack(side="right",in_=self.button_frame,padx=5)
        self.filter_data_button = ttk.Button(self.production_tab, text="filter", command=self.filter_data)
        self.filter_data_button.pack(side="right",in_=self.button_frame)
        self.button_frame.pack(side="top",fill="x",in_=self.production_tab)

        self.tree_frame = tk.Frame(self.production_tab)
        self.data_scrollbar_x = tk.Scrollbar(self.tree_frame,orient='horizontal')
        self.data_scrollbar_x.pack(
            in_=self.tree_frame, side=tk.BOTTOM,fill=tk.X
        )
        self.data_scrollbar_y = tk.Scrollbar(self.tree_frame)
        self.data_scrollbar_y.pack(
            in_=self.tree_frame, side=tk.RIGHT,fill=tk.Y
        )
        self.production_tree = ttk.Treeview(self.production_tab, columns=("Machine ID", "Equipment Type", "Batch ID", "Product Type", "Start date", "End date", "Units Produced", "Result", "Remarks"),
                                            show="headings",xscrollcommand=self.data_scrollbar_x.set, yscrollcommand=self.data_scrollbar_y.set)
        self.production_tree.heading("Machine ID", text="Machine ID")
        self.production_tree.heading("Equipment Type", text="Equipment Type")
        self.production_tree.heading("Batch ID", text="Batch ID")
        self.production_tree.heading("Product Type", text="Product Type")
        self.production_tree.heading("Start date", text="Start date")
        self.production_tree.heading("End date", text="End date")
        self.production_tree.heading("Result", text="Result")
        self.production_tree.heading("Remarks", text="Remarks")
        self.production_tree.pack(fill="both", expand=True, in_=self.tree_frame)
        self.data_scrollbar_x.config(command=self.production_tree.xview)
        self.data_scrollbar_y.config(command=self.production_tree.yview)
        self.load_production_data()
        self.tree_frame.pack(side="top",fill="both", expand=True,in_=self.production_tab)

    def setup_log_tab(self):
        """
        Setup the log tab.
        """
        ttk.Label(self.log_tab, text="Runtime logs", font=("Arial", 16)).pack(pady=10)
        self.log_text = tk.Text(self.log_tab, wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=10)

    def add_log(self, message):
        self.log_text.insert(tk.END, f"{datetime.now()}: {message}\n\n")
        logging.info(message)

    def setup_report_tab(self):
        """
        Setup the reports tab.
        """
        ttk.Label(self.report_tab, text="Reports", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.report_tab, text="Generate Summary Report", command=self.generate_report).pack(pady=5)
        self.report_text = tk.Text(self.report_tab, wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)


    def on_tree_select(self, event):
        self.selected_item = self.production_tree.selection()
        if self.selected_item and self.user.role!="operator":
            self.edit_data_button.config(state=tk.NORMAL)
        else:
            self.edit_data_button.config(state=tk.DISABLED)

    def load_production_data(self):
        """
        Load production data from a CSV file.
        """
        try:
            self.jobs = self.production_data.production_data
            self.add_log("Sucessfully loaded data production data from database")
            self.populate_production_data(self.jobs)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def populate_production_data(self, production_data):
        """
        Populate the production data treeview.
        """
        for item in self.production_tree.get_children():
            self.production_tree.delete(item)
        for machine in production_data:
            self.production_tree.insert("", "end", values=(
                machine["machine_id"],
                machine["machine_type"],
                machine["batch_id"],
                machine["product_type"],
                machine["start_date"],
                machine["end_date"],
                machine["units"],
                machine["result"],
                machine["remarks"]
                )
            )
        self.add_log("Populated latest production data to UI")

    def generate_report(self):
        """
        Generate a summary report.
        """
        self.report_text.delete(1.0, tk.END)
        report_list = []
        for child in self.production_tree.get_children():
            report_dict = {}
            for col, item in zip(self.production_tree["columns"], self.production_tree.item(child)["values"]):
                report_dict.update({col:item})
            report_list.append(report_dict)
        if not report_list:
            self.report_text.insert(tk.END, "No data available to generate a report.")
            return

        report_lines = []
        for i, data_row in enumerate(report_list):
            report_lines.append(f"row_{i}: {{")
            report_lines.append(f"\t{data_row}")
            report_lines.append(f"}}{"," if data_row != report_list[-1] else ""}")

        self.report_text.insert(tk.END, "\n".join(report_lines))

        save_location = filedialog.askdirectory()

        # Writing to the CSV file
        with open(f"{save_location}/report.json", mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(report_list[0].keys()))
            
            # Write the header
            writer.writeheader()
            
            # Write the data
            writer.writerows(report_list)

        self.add_log(f"Generated report and stored at location : {save_location}/report.json")

    def edit_data(self):
        prod_data = {}
        selected = self.production_tree.focus()
        if len(self.production_tree.selection()) != 1:
            messagebox.showerror("Invalid selection","Unable to edit multiple entries at once!!!")
        table_data = self.production_tree.item(self.production_tree.selection())["values"]
        prod_data_template = self.prod_data
        for i, (key, value) in enumerate(prod_data_template.items()):
            prod_data[key] = table_data[i]
        dialog = CustomDialog(self,"Edit data",prod_data,self.ui_data,self.permission_data,self.combobox_data)
        if dialog.result is None:
            self.add_log("Cancel edit data")
            return
        state = self.production_data.update_result(dialog.result)
        if state[0]:
            self.production_tree.item(selected, values=[value for key, value in dialog.result.items()])
        self.add_log(state[1])

        

    def add_data(self):
        dialog = CustomDialog(self,"Add data",self.prod_data,self.ui_data,self.permission_data,self.combobox_data)
        if dialog.result is None:
            self.add_log("Cancel add data")
            return
        result = dialog.result
        state = self.production_data.add_data(result)
        if state[0]:
            self.populate_production_data(self.jobs)
        self.add_log(state[1])

    def filter_data(self):
        dialog = FilterDialog(self,"FIlter data",list(self.permission_data.keys()),self.production_data)
        if dialog.result is None:
            self.add_log("Cancel filter data")
            return
        filtered_data = self.production_data.filter_data(dialog.result[0],dialog.result[1])
        self.populate_production_data(filtered_data)
        self.add_log(f"Filtered data by {dialog.result[0]} target is {dialog.result[1]}")
        self.filter_data_button.destroy()
        self.reset_filter_button = ttk.Button(self.production_tab, text="reset", command=self.reset_filter)
        self.reset_filter_button.pack(side="right",in_=self.button_frame)

    def reset_filter(self):
        self.populate_production_data(self.jobs)
        self.reset_filter_button.destroy()
        self.filter_data_button = ttk.Button(self.production_tab, text="filter", command=self.filter_data)
        self.filter_data_button.pack(side="right",in_=self.button_frame)
        self.add_log("Reset filter")



    def set_user_permissions(self):
        if self.user.role == "operator":
            self.add_data_button.config(state=tk.NORMAL)
            self.permission_data =  {'machine_id': 'normal', 'machine_type': 'normal', 'batch_id': 'normal', 'product_type': 'readonly', 'start_date': 'normal', 'end_date': 'normal', 'units': 'normal', 'result': 'normal', 'remarks': 'normal'}
        if self.user.role == "qc_inspector":
            self.add_data_button.config(state=tk.DISABLED)
            self.ui_data =  {'machine_id': 'entry', 'machine_type': 'entry', 'batch_id': 'entry', 'product_type': 'entry', 'start_date': 'entry', 'end_date': 'entry', 'units': 'entry', 'result': 'combobox', 'remarks': 'entry'}
            self.permission_data =  {'machine_id': 'readonly', 'machine_type': 'readonly', 'batch_id': 'readonly', 'product_type': 'readonly', 'start_date': 'readonly', 'end_date': 'readonly', 'units': 'readonly', 'result': 'normal', 'remarks': 'normal'}
        if self.user.role == "admin":
            self.add_data_button.config(state=tk.NORMAL)
            self.permission_data =  {'machine_id': 'normal', 'machine_type': 'normal', 'batch_id': 'normal', 'product_type': 'readonly', 'start_date': 'normal', 'end_date': 'normal', 'units': 'normal', 'result': 'normal', 'remarks': 'normal'}


if __name__ == "__main__":
    app = ProductionMonitoringApp()
    app.mainloop()
