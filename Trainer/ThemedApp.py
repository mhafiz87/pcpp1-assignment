import tkinter as tk
from tkinter import ttk


class ThemedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Themed Application with TTK Styling")
        self.geometry("800x600")

        # Set default theme
        self.style = ttk.Style(self)
        self.available_themes = ["clam", "alt"]  # Define available themes
        self.current_theme = tk.StringVar(value=self.available_themes[0])
        self.apply_theme(self.current_theme.get())

        # Create the interface
        self.create_interface()

    def apply_theme(self, theme_name):
        """
        Apply the selected theme to the application.
        """
        self.style.theme_use(theme_name)

    def create_interface(self):
        """
        Create the main interface with theme selection and demonstration of ttk widgets.
        """
        # Theme Selection Dropdown
        ttk.Label(self, text="Select Theme:", font=("Arial", 14)).pack(pady=10)
        theme_selector = ttk.Combobox(
            self, textvariable=self.current_theme, values=self.available_themes, state="readonly"
        )
        theme_selector.pack(pady=5)
        theme_selector.bind("<<ComboboxSelected>>", self.change_theme)

        # Create a frame for demonstration widgets
        demo_frame = ttk.Frame(self, padding=10)
        demo_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add widgets to demo the theme
        ttk.Label(demo_frame, text="Demonstration of TTK Widgets", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        ttk.Label(demo_frame, text="Enter your name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        name_entry = ttk.Entry(demo_frame, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(demo_frame, text="Select your role:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        role_combobox = ttk.Combobox(demo_frame, values=["Admin", "User", "Guest"], state="readonly")
        role_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(demo_frame, text="Enable features:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        feature1_var = tk.BooleanVar()
        feature2_var = tk.BooleanVar()
        ttk.Checkbutton(demo_frame, text="Feature 1", variable=feature1_var).grid(row=3, column=1, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(demo_frame, text="Feature 2", variable=feature2_var).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(demo_frame, text="Submit", command=lambda: self.show_message(name_entry.get(), role_combobox.get())).grid(
            row=5, column=0, columnspan=2, pady=10
        )

    def change_theme(self, event):
        """
        Change the application's theme based on user selection.
        """
        selected_theme = self.current_theme.get()
        self.apply_theme(selected_theme)

    def show_message(self, name, role):
        """
        Display a message showing entered details.
        """
        message = f"Hello, {name}! Your role is {role}."
        ttk.Label(self, text=message, font=("Arial", 12), foreground="green").pack(pady=10)


if __name__ == "__main__":
    app = ThemedApp()
    app.mainloop()
