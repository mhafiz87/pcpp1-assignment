import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .car import car_data


class RentalCarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Rental App")
        self.resizable(True, True)

        self.create_login_screen()
        self.car_selection_header = [
            "brand",
            "model",
            "engine_type",
            "seat_capacity",
            "status",
        ]

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
            self.login_frame, text="Login", command=self.create_page_selection_screen
        )

        login_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        username_label.grid(row=1, column=0, padx=5, pady=5)
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label.grid(row=2, column=0, padx=5, pady=5)
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.login_frame.pack(pady=20)

    def create_page_selection_screen(self):
        self.login_frame.destroy()
        self.tab_control = ttk.Notebook(self)

        self.car_selection_tab = ttk.Frame(self.tab_control)
        self.car_monitor_tab = ttk.Frame(self.tab_control)
        self.customer_profile_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.car_selection_tab, text="Car Selection")
        self.tab_control.add(self.car_monitor_tab, text="Car Monitoring")
        self.tab_control.add(self.customer_profile_tab, text="Customer Profile")
        self.tab_control.pack(expand=1, fill="both")

        self.create_car_selection_screen()
        self.create_car_monitoring_screen()
        self.create_customer_profile_screen()

    def perform_login(self):
        pass

    def create_car_selection_screen(self):
        filter_column = 1
        ttk.Label(self.car_selection_tab, text="Car Selection").grid(row=0, column=0)
        ttk.Label(self.car_selection_tab, text="Car Filter").grid(row=0, column=filter_column)

        ttk.Label(self.car_selection_tab, text="Brand").grid(row=1, column=filter_column)
        ttk.Label(self.car_selection_tab, text="Model").grid(row=3, column=filter_column)
        ttk.Label(self.car_selection_tab, text="Engine").grid(row=5, column=filter_column)
        ttk.Label(self.car_selection_tab, text="Seat").grid(row=7, column=filter_column)
        ttk.Label(self.car_selection_tab, text="Status").grid(row=9, column=filter_column)

        self.reset_select_filter()

        ttk.Button(
            self.car_selection_tab, text="Clear Filter", command=self.reset_select_filter
        ).grid(row=12, column=filter_column)

        self.car_selection_tree = ttk.Treeview(
            self.car_selection_tab,
            columns=list(self.car_selection_header),
            show="headings",
        )
        for heading in self.car_selection_header:
            self.car_selection_tree.heading(heading, text=heading)
        self.car_selection_tree.grid(
            row=1, column=0, rowspan=10, columnspan=1, padx=5, pady=5
        )

        ttk.Button(
            self.car_selection_tab, text="Select", command=self.select_car_for_rental
        ).grid(row=12, column=0, columnspan=1, padx=5, pady=5)

        self.populate_car_selection_tree(data=self.car_selection_header)

    def reset_select_filter(self):
        filter_column = 1
        try:
            self.car_selection_filter_brand.destroy()
            self.car_selection_filter_model.destroy()
            self.car_selection_filter_engine.destroy()
            self.car_selection_filter_seat.destroy()
            self.car_selection_filter_status.destroy()
        except AttributeError:
            print("Widget yet to exist.")

        self.car_selection_filter_brand = ttk.Combobox(self.car_selection_tab)
        self.car_selection_filter_model = ttk.Combobox(self.car_selection_tab)
        self.car_selection_filter_engine = ttk.Combobox(self.car_selection_tab)
        self.car_selection_filter_seat = ttk.Combobox(self.car_selection_tab)
        self.car_selection_filter_status = ttk.Combobox(self.car_selection_tab)

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
        print(info)
        self.car_selection_filter_brand["values"] = list(info["brand"])
        self.car_selection_filter_model["values"] = list(info["model"])
        self.car_selection_filter_engine["values"] = list(info["engine_type"])
        self.car_selection_filter_seat["values"] = list(info["seat_capacity"])
        self.car_selection_filter_status["values"] = list(info["status"])

    def populate_car_selection_tree(self, data: list[str]):
        self.car_selection_tree.delete(*self.car_selection_tree.get_children())
        for item in car_data.load_car_data():
            self.car_selection_tree.insert(
                "", "end", values=(tuple(item[info] for info in data))
            )

    def create_car_monitoring_screen(self):
        ttk.Label(self.car_monitor_tab, text="Car Monitoring").grid(
            row=0, column=0, columnspan=1, padx=5, pady=5
        )

    def select_car_for_rental(self):
        print(self.car_selection_tree.item(self.car_selection_tree.focus()))

    def create_car_return_screen(self):
        pass

    def create_customer_registration_screen(self):
        pass

    def create_customer_profile_screen(self):
        ttk.Label(self.customer_profile_tab, text="Customer Profile").grid(
            row=0, column=0, padx=5, pady=5
        )
        # self.secondary_frame_label.destroy()
        # self.secondary_frame_label = ttk.Label(
        #     self.secondary_frame, text="Customer Profile Screen"
        # )
        # self.secondary_frame_label.pack(pady=10)

    def create_rental_history_screen(self):
        pass


if __name__ == "__main__":
    app = RentalCarApp()
    app.mainloop()
