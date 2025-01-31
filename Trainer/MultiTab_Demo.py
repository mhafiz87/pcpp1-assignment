import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class MultiTabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Tab Application with Dropdown Menu")
        self.geometry("800x600")

        # Create the menu bar
        self.create_menu()

        # Create the tabbed interface
        self.create_tabs()

    def create_menu(self):
        """
        Create a dropdown menu bar.
        """
        menubar = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_tabs(self):
        """
        Create tabs for the application.
        """
        self.tab_control = ttk.Notebook(self)

        # Add tabs
        self.home_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.about_tab = ttk.Frame(self.tab_control)

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
        Populate the Home tab with widgets.
        """
        ttk.Label(self.home_tab, text="Welcome to the Home Tab", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.home_tab, text="Click Me", command=self.home_button_clicked).pack(pady=10)

    def populate_settings_tab(self):
        """
        Populate the Settings tab with dropdowns and options.
        """
        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.settings_tab, text="Select Theme:").pack(pady=5)
        self.theme_combobox = ttk.Combobox(self.settings_tab, values=["Light", "Dark"], state="readonly")
        self.theme_combobox.set("Light")  # Default value
        self.theme_combobox.pack(pady=5)

        ttk.Label(self.settings_tab, text="Enable Features:").pack(pady=5)
        self.feature1_var = tk.BooleanVar()
        self.feature2_var = tk.BooleanVar()
        ttk.Checkbutton(self.settings_tab, text="Feature 1", variable=self.feature1_var).pack()
        ttk.Checkbutton(self.settings_tab, text="Feature 2", variable=self.feature2_var).pack()

    def populate_about_tab(self):
        """
        Populate the About tab with information.
        """
        ttk.Label(self.about_tab, text="About this Application", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.about_tab, text="This is a multi-tab example using tkinter.", wraplength=600).pack(pady=10)

    def home_button_clicked(self):
        """
        Handle button click on the Home tab.
        """
        messagebox.showinfo("Home Button", "Button on the Home tab clicked!")

    def open_file(self):
        """
        Open a file dialog.
        """
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            messagebox.showinfo("File Opened", f"You selected: {file_path}")

    def save_file(self):
        """
        Open a save file dialog.
        """
        file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("Demo content saved!")
            messagebox.showinfo("File Saved", f"File saved at: {file_path}")

    def show_about(self):
        """
        Display the About dialog.
        """
        messagebox.showinfo("About", "This is a demo application showcasing tkinter features.")


if __name__ == "__main__":
    app = MultiTabApp()
    app.mainloop()
