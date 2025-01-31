import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from colored import Fore, Style
from tkcalendar import Calendar

from .car import CarData
from .customer import CustomerData
from .database import Database
from .logger import logger
from .staff import StaffData

car_data = CarData()
customer_data = CustomerData()
staff_data = StaffData()
database = Database()


class RentalCarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        database.create_tables()
        database.populate_table("cars")
        self.title("Car Rental App")
        self.resizable(True, True)

        self.create_login_screen()
        self.car_selection_hide_column = ["ID", "start_date", "end_date"]
        self.car_selection_header = list(car_data.load_car_data()[0].keys())
        self.car_monitor_header = list(car_data.load_car_data()[0].keys())
        self.customer_header = list(customer_data.load_customer_data()[0].keys())

    def destroy_screens(self):
        try:
            self.login_frame.destroy()
        except AttributeError:
            print("Widget is not available.")
        try:
            self.rental_screen.destroy()
        except AttributeError:
            print("Widget is not available.")

    def create_login_screen(self):
        self.current_user = tk.StringVar(self)
        self.current_password = tk.StringVar(self)

        self.login_frame = ttk.Frame(self)

        login_label = ttk.Label(self.login_frame, text="Login", font=("Arial", 25))
        username_label = ttk.Label(self.login_frame, text="Username:")
        username_entry = ttk.Entry(self.login_frame, textvariable=self.current_user)

        password_label = ttk.Label(self.login_frame, text="Password:")
        password_entry = ttk.Entry(
            self.login_frame, textvariable=self.current_password, show="*"
        )

        # login_button = ttk.Button(self.login_frame, text="Login", command=self.perform_login)
        login_button = ttk.Button(
            self.login_frame, text="Login", command=self.validate_login
        )

        login_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        username_label.grid(row=1, column=0, padx=5, pady=5)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label.grid(row=2, column=0, padx=5, pady=5)
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.login_frame.pack(pady=20)

        self.update()
        print(self.geometry())

    def validate_login(self):
        self.create_page_selection_screen()
        return
        status = staff_data.is_staff(self.current_user.get(), self.current_password.get())
        if status:
            self.create_page_selection_screen()
        else:
            logger.warning(f"{Style.bold}{Fore.red}Invalid username or password.{Style.reset}")
            messagebox.showwarning("Warning!!!", "Invalid username or password.")

    def create_page_selection_screen(self):
        self.destroy_screens()
        self.tab_control = ttk.Notebook(self)

        self.car_selection_tab = ttk.Frame(self.tab_control)
        self.car_monitor_tab = ttk.Frame(self.tab_control)
        self.customer_profile_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.car_selection_tab, text="Car Selection")
        self.tab_control.add(self.car_monitor_tab, text="Car Monitoring")
        self.tab_control.add(self.customer_profile_tab, text="Customer Profile")
        self.tab_control.pack(expand=1, fill="both")

        # for i, tab in enumerate(self.tab_control.winfo_children()):
        #     tab_text = self.tab_control.tab(i, 'text')
        #     print(f"Tab {i} Text: {tab_text}")

        self.create_car_selection_screen()
        self.create_car_monitoring_screen()
        self.create_customer_profile_screen()


    def perform_login(self):
        pass

    def create_car_selection_screen(self):
        filter_column = 2
        ttk.Label(self.car_selection_tab, text="Car Selection").grid(row=0, column=0)
        ttk.Label(self.car_selection_tab, text="Car Filter").grid(
            row=0, column=filter_column
        )

        ttk.Label(self.car_selection_tab, text="Brand").grid(
            row=1, column=filter_column
        )
        ttk.Label(self.car_selection_tab, text="Model").grid(
            row=3, column=filter_column
        )
        ttk.Label(self.car_selection_tab, text="Engine").grid(
            row=5, column=filter_column
        )
        ttk.Label(self.car_selection_tab, text="Seat").grid(row=7, column=filter_column)
        ttk.Label(self.car_selection_tab, text="Status").grid(
            row=9, column=filter_column
        )
        self.reset_select_filter()

        ttk.Button(
            self.car_selection_tab,
            text="Clear Filter",
            command=self.reset_select_filter,
        ).grid(row=12, column=filter_column)

        self.car_selection_tree = ttk.Treeview(
            self.car_selection_tab,
            columns=list(self.car_selection_header),
            show="headings",
        )
        # https://stackoverflow.com/questions/33290969/hiding-treeview-columns-in-tkinter
        display_column = []
        for col in self.car_selection_tree["columns"]:
            if not col in self.car_selection_hide_column:
                display_column.append(col)
        self.car_selection_tree["displaycolumns"] = display_column
        # for heading in self.car_selection_header:
        #     self.car_selection_tree.heading(heading, text=heading, anchor=tk.CENTER)
        self.car_selection_tree.grid(
            row=1, column=0, rowspan=10, columnspan=1, padx=5, pady=5
        )

        car_tree_vert_scrollbar = ttk.Scrollbar(self.car_selection_tab, orient="vertical", command=self.car_selection_tree.yview)
        car_tree_vert_scrollbar.grid(row=1, column=1, rowspan=10, padx=5, pady=5, sticky="W")
        self.car_selection_tree.configure(yscrollcommand=car_tree_vert_scrollbar.set)

        self.populate_car_selection_tree(data=self.car_selection_header)

        ttk.Button(
            self.car_selection_tab,
            text="Select",
            command=lambda: self.select_car_for_rental(
                self.car_selection_tree.item(self.car_selection_tree.focus())
            ),
        ).grid(row=12, column=0, columnspan=1, padx=5, pady=5)

        self.geometry("699x322+340+288")

    def reset_select_filter(self):
        filter_column = 2
        try:
            self.car_selection_filter_brand.destroy()
            self.car_selection_filter_model.destroy()
            self.car_selection_filter_engine.destroy()
            self.car_selection_filter_seat.destroy()
            self.car_selection_filter_status.destroy()
        except AttributeError:
            print("Widget yet to exist.")

        self.car_selection_filter_brand = ttk.Combobox(
            self.car_selection_tab, justify="center"
        )
        self.car_selection_filter_model = ttk.Combobox(
            self.car_selection_tab, justify="center"
        )
        self.car_selection_filter_engine = ttk.Combobox(
            self.car_selection_tab, justify="center"
        )
        self.car_selection_filter_seat = ttk.Combobox(
            self.car_selection_tab, justify="center"
        )
        self.car_selection_filter_status = ttk.Combobox(
            self.car_selection_tab, justify="center"
        )

        self.car_selection_filter_brand.grid(row=2, column=filter_column)
        self.car_selection_filter_model.grid(row=4, column=filter_column)
        self.car_selection_filter_engine.grid(row=6, column=filter_column)
        self.car_selection_filter_seat.grid(row=8, column=filter_column)
        self.car_selection_filter_status.grid(row=10, column=filter_column)

        self.populate_car_selection_filter(data=car_data.load_car_data())

    def populate_car_selection_filter(self, data: list[str]):
        info = {}
        for items in data[0]:
            if items != "ID":
                info[items] = set("")
        for items in data:
            for key, value in items.items():
                for temp in info.keys():
                    if key == temp:
                        info[key].add(value)
                        break
        # print(info)
        self.car_selection_filter_brand["values"] = list(info["brand"])
        self.car_selection_filter_model["values"] = list(info["model"])
        self.car_selection_filter_engine["values"] = list(info["engine_type"])
        self.car_selection_filter_seat["values"] = list(info["seat_capacity"])
        self.car_selection_filter_status["values"] = list(info["status"])

        self.car_selection_filter_brand.configure(justify="center")
        self.car_selection_filter_model.configure(justify="center")
        self.car_selection_filter_engine.configure(justify="center")
        self.car_selection_filter_seat.configure(justify="center")
        self.car_selection_filter_status.configure(justify="center")

    def populate_car_selection_tree(self, data: list[str]):
        self.car_selection_tree.delete(*self.car_selection_tree.get_children())
        for item in car_data.load_car_data():
            if item["status"] == "available":
                self.car_selection_tree.insert(
                    "", "end", values=(tuple(item[info] for info in data))
                )
        for col in self.car_selection_tree["columns"]:
            self.car_selection_tree.column(col, anchor="center", width=100)

    def create_car_monitoring_screen(self):
        self.tab_control.tab
        ttk.Label(self.car_monitor_tab, text="Car Monitoring").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.car_monitoring_tree = ttk.Treeview(
            self.car_monitor_tab,
            columns=list(self.car_monitor_header),
            show="headings",
        )
        for heading in self.car_monitor_header:
            self.car_monitoring_tree.heading(heading, text=heading, anchor=tk.CENTER)
        self.car_monitoring_tree.grid(
            row=1, column=0, rowspan=10, columnspan=1, padx=5, pady=5
        )

        self.populate_car_monitoring_tree(data=self.car_monitor_header)

        car_tree_vert_scrollbar = ttk.Scrollbar(self.car_monitor_tab, orient="vertical", command=self.car_monitoring_tree.yview)
        car_tree_vert_scrollbar.grid(row=1, column=1, rowspan=10, padx=5, pady=5, sticky="W")
        self.car_monitoring_tree.configure(yscrollcommand=car_tree_vert_scrollbar.set)

        print(self.geometry())

    def populate_car_monitoring_tree(self, data, filter=None):
        self.car_monitoring_tree.delete(*self.car_monitoring_tree.get_children())
        for item in car_data.load_car_data():
            self.car_monitoring_tree.insert(
                "", "end", values=(tuple(item[info] for info in data))
            )
        for col in self.car_monitoring_tree["columns"]:
            self.car_monitoring_tree.column(col, anchor="center", width=100)

    def select_car_for_rental(self, data):
        print(data)
        if data["values"] == "":
            messagebox.showwarning("Warning!!!", "Please select a car first.")
            return
        self.temp_rental_info = data
        self.tab_control.destroy()
        self.rental_screen = ttk.Frame(self)
        ttk.Label(self.rental_screen, text="Rental Screen", font=("Arial", 25)).grid(
            row=0, column=0
        )

        ttk.Separator(self.rental_screen, orient="horizontal").grid(
            row=1, column=0, columnspan=10, sticky="EW"
        )

        self.rental_brand = tk.StringVar(self)
        self.rental_model = tk.StringVar(self)
        self.rental_engine = tk.StringVar(self)
        self.rental_seat = tk.StringVar(self)
        self.rental_status = tk.StringVar(self)
        self.rental_start_date = tk.StringVar(self)
        self.rental_end_date = tk.StringVar(self)

        ttk.Label(self.rental_screen, text="Brand").grid(
            row=2, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Model").grid(
            row=3, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Engine").grid(
            row=4, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Seat").grid(
            row=5, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Status").grid(
            row=6, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Start Date").grid(
            row=7, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="End Date").grid(
            row=8, column=0, sticky="W", padx=10
        )

        rental_brand_entry = ttk.Entry(
            self.rental_screen, textvariable=self.rental_brand
        )
        rental_brand_model = ttk.Entry(
            self.rental_screen, textvariable=self.rental_model
        )
        rental_brand_engine = ttk.Entry(
            self.rental_screen, textvariable=self.rental_engine
        )
        rental_brand_seat = ttk.Entry(self.rental_screen, textvariable=self.rental_seat)
        rental_brand_status = ttk.Entry(
            self.rental_screen, textvariable=self.rental_status
        )
        rental_start_date_entry = ttk.Entry(
            self.rental_screen, textvariable=self.rental_start_date
        )
        rental_start_end_entry = ttk.Entry(
            self.rental_screen, textvariable=self.rental_end_date
        )

        try:
            rental_brand_entry.insert(0, self.temp_rental_info["values"][1])
            rental_brand_model.insert(0, self.temp_rental_info["values"][2])
            rental_brand_engine.insert(0, self.temp_rental_info["values"][3])
            rental_brand_seat.insert(0, self.temp_rental_info["values"][4])
            rental_brand_status.insert(0, self.temp_rental_info["values"][5])

            rental_brand_entry.configure(state="readonly")
            rental_brand_model.configure(state="readonly")
            rental_brand_engine.configure(state="readonly")
            rental_brand_seat.configure(state="readonly")
            rental_brand_status.configure(state="readonly")
        except IndexError:
            print("Empty Data")

        rental_brand_entry.grid(row=2, column=1, sticky="W", padx=10)
        rental_brand_model.grid(row=3, column=1, sticky="W", padx=10)
        rental_brand_engine.grid(row=4, column=1, sticky="W", padx=10)
        rental_brand_seat.grid(row=5, column=1, sticky="W", padx=10)
        rental_brand_status.grid(row=6, column=1, sticky="W", padx=10)
        rental_start_date_entry.grid(row=7, column=1, sticky="W", padx=10)
        rental_start_end_entry.grid(row=8, column=1, sticky="W", padx=10)

        ttk.Separator(self.rental_screen, orient="horizontal").grid(
            row=9, column=0, columnspan=10, sticky="EW"
        )

        self.rental_name = tk.StringVar(self)
        self.rental_contact = tk.StringVar(self)
        self.rental_address = tk.StringVar(self)
        self.rental_email = tk.StringVar(self)

        ttk.Label(self.rental_screen, text="Full Name").grid(
            row=10, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Contact").grid(
            row=11, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Address").grid(
            row=12, column=0, sticky="W", padx=10
        )
        ttk.Label(self.rental_screen, text="Email").grid(
            row=13, column=0, sticky="W", padx=10
        )

        ttk.Entry(self.rental_screen, textvariable=self.rental_name).grid(
            row=10, column=1, sticky="W", padx=10
        )
        ttk.Entry(self.rental_screen, textvariable=self.rental_contact).grid(
            row=11, column=1, sticky="W", padx=10
        )
        ttk.Entry(self.rental_screen, textvariable=self.rental_address).grid(
            row=12, column=1, sticky="W", padx=10
        )
        ttk.Entry(self.rental_screen, textvariable=self.rental_email).grid(
            row=13, column=1, sticky="W", padx=10
        )

        ttk.Button(
            self.rental_screen, text="Rent", command=self.rental_confirmation_screen
        ).grid(row=14, column=0, padx=10)
        ttk.Button(
            self.rental_screen, text="Cancel", command=self.create_page_selection_screen
        ).grid(row=14, column=1, padx=10)

        self.rental_screen.pack()

        self.geometry("358x309+340+288")

    def rental_confirmation_screen(self):
        customer_rental_data = {
            "full_name": self.rental_name.get(),
            "contact": self.rental_contact.get(),
            "address": self.rental_address.get(),
            "email": self.rental_email.get(),
            "car": self.temp_rental_info["values"][0],
            "start_date": self.rental_start_date.get(),
            "end_date": self.rental_end_date.get(),
        }
        car_rental_data = {
            "ID": self.temp_rental_info["values"][0],
            "start_date": self.rental_start_date.get(),
            "end_date": self.rental_end_date.get(),
        }
        customer_data.update_customer_data(customer_rental_data)
        car_data.update_car_data(car_rental_data)
        self.create_page_selection_screen()
        self.tab_control.select(1)

    def create_customer_profile_screen(self):
        ttk.Label(self.customer_profile_tab, text="Customer Profile").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.customer_tree = ttk.Treeview(
            self.customer_profile_tab,
            columns=list(self.customer_header),
            show="headings",
        )
        for heading in self.customer_header:
            self.customer_tree.heading(heading, text=heading, anchor=tk.CENTER)
        self.customer_tree.grid(
            row=1, column=0, rowspan=10, columnspan=1, padx=5, pady=5
        )
        self.populate_customer_tree(data=self.customer_header)

    def populate_customer_tree(self, data):
        self.customer_tree.delete(*self.customer_tree.get_children())
        for item in customer_data.load_customer_data():
            self.customer_tree.insert(
                "", "end", values=(tuple(item[info] for info in data))
            )
        for col in self.customer_tree["columns"]:
            self.customer_tree.column(col, anchor="center")
        return

    def create_rental_history_screen(self):
        pass


if __name__ == "__main__":
    app = RentalCarApp()
    app.mainloop()
    app.mainloop()
