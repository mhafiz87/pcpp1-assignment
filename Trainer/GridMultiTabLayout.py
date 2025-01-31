import tkinter as tk
from tkinter import ttk, messagebox


class MultiTabGridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Tab Application with Grid Layout")
        self.geometry("800x600")

        # Create tabs
        self.create_tabs()

    def create_tabs(self):
        """
        Create a tabbed interface with multiple tabs.
        """
        self.tab_control = ttk.Notebook(self)

        # Create individual tabs
        self.home_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.about_tab = ttk.Frame(self.tab_control)

        # Add tabs to the tab control
        self.tab_control.add(self.home_tab, text="Home")
        self.tab_control.add(self.settings_tab, text="Settings")
        self.tab_control.add(self.about_tab, text="About")
        self.tab_control.pack(expand=1, fill="both")

        # Populate each tab
        self.populate_home_tab()
        self.populate_settings_tab()
        self.populate_about_tab()

    def populate_home_tab(self):
        """
        Populate the Home tab with widgets arranged in a grid layout.
        """
        ttk.Label(self.home_tab, text="Welcome to the Home Tab", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.home_tab, text="Enter your name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.home_tab, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.home_tab, text="Select your role:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.role_combobox = ttk.Combobox(self.home_tab, values=["Admin", "User", "Guest"], state="readonly")
        self.role_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self.home_tab, text="Submit", command=self.submit_home_form).grid(row=3, column=0, columnspan=2, pady=10)

    def populate_settings_tab(self):
        """
        Populate the Settings tab with widgets arranged in a grid layout.
        """
        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.settings_tab, text="Enable Feature 1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.feature1_var = tk.BooleanVar()
        ttk.Checkbutton(self.settings_tab, variable=self.feature1_var).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.settings_tab, text="Enable Feature 2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.feature2_var = tk.BooleanVar()
        ttk.Checkbutton(self.settings_tab, variable=self.feature2_var).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self.settings_tab, text="Save Settings", command=self.save_settings).grid(row=3, column=0, columnspan=2, pady=10)

    def populate_about_tab(self):
        """
        Populate the About tab with widgets arranged in a grid layout.
        """
        ttk.Label(self.about_tab, text="About", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        about_text = (
            "This is a multi-tab tkinter application.\n"
            "It demonstrates the use of the grid layout manager for\n"
            "effective widget placement within tabs."
        )
        ttk.Label(self.about_tab, text=about_text, wraplength=600, justify="left").grid(row=1, column=0, padx=10, pady=5)

    def submit_home_form(self):
        """
        Handle form submission in the Home tab.
        """
        name = self.name_entry.get().strip()
        role = self.role_combobox.get().strip()

        if not name or not role:
            messagebox.showerror("Error", "Please enter your name and select a role.")
        else:
            messagebox.showinfo("Form Submitted", f"Welcome, {name}! Role: {role}")

    def save_settings(self):
        """
        Handle settings save action in the Settings tab.
        """
        feature1_status = "enabled" if self.feature1_var.get() else "disabled"
        feature2_status = "enabled" if self.feature2_var.get() else "disabled"
        messagebox.showinfo("Settings Saved", f"Feature 1: {feature1_status}\nFeature 2: {feature2_status}")


if __name__ == "__main__":
    app = MultiTabGridApp()
    app.mainloop()
