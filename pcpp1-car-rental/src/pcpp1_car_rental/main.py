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
        ttk.Label(self.car_selection_tab, text="Car Selection").grid(
            row=0, column=0, columnspan=1, padx=5, pady=5
        )
        ttk.Label(self.car_selection_tab, text="Car Filter").grid(
            row=0, column=filter_column, padx=5, pady=5
        )

        self.car_selection_filter_combobox = []
        for index in range(1, (len(self.car_selection_header) * 2) + 1):
            if (index) % 2 == 0:
                self.car_selection_filter_combobox.append(
                    ttk.Combobox(self.car_selection_tab).grid(
                        row=index, column=filter_column, padx=5, pady=5
                    )
                )
            else:
                ttk.Label(
                    self.car_selection_tab, text=self.car_selection_header[index // 2]
                ).grid(row=index, column=filter_column, padx=5, pady=5)

        self.car_selection_tree = ttk.Treeview(
            self.car_selection_tab,
            columns=list(self.car_selection_header),
            show="headings",
        )
        for heading in self.car_selection_header:
            self.car_selection_tree.heading(heading, text=heading)
        self.car_selection_tree.grid(
            row=1, column=0, rowspan=20, columnspan=1, padx=5, pady=5
        )
        self.populate_car_selection_tree(data=self.car_selection_header)

        ttk.Button(
            self.car_selection_tab, text="Select", command=self.load_car_data
        ).grid(row=11, column=0, columnspan=1, padx=5, pady=5)

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

    def load_car_data(self):
        pass

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
