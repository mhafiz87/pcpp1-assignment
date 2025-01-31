import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class TkinterWidgetsDemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Widgets Demo")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        """
        Create and display all the widgets in tkinter.
        """
        ttk.Label(self, text="Tkinter Widgets Showcase", font=("Arial", 20)).pack(pady=10)

        # Button Widget
        ttk.Button(self, text="Click Me", command=self.button_clicked).pack(pady=10)

        # Label Widget
        ttk.Label(self, text="This is a Label").pack(pady=10)

        # Entry Widget
        ttk.Label(self, text="Enter Text Below:").pack(pady=5)
        self.entry_widget = ttk.Entry(self, width=30)
        self.entry_widget.pack(pady=5)

        # Combobox Widget
        ttk.Label(self, text="Select an Option:").pack(pady=5)
        self.combobox_widget = ttk.Combobox(self, values=["Option 1", "Option 2", "Option 3"], state="readonly")
        self.combobox_widget.pack(pady=5)

        # RadioButton Widget
        ttk.Label(self, text="Select a Choice:").pack(pady=5)
        self.radio_value = tk.StringVar(value="Choice 1")
        ttk.Radiobutton(self, text="Choice 1", variable=self.radio_value, value="Choice 1").pack()
        ttk.Radiobutton(self, text="Choice 2", variable=self.radio_value, value="Choice 2").pack()

        # Checkbutton Widget
        ttk.Label(self, text="Select Your Preferences:").pack(pady=5)
        self.check_value_1 = tk.BooleanVar()
        self.check_value_2 = tk.BooleanVar()
        ttk.Checkbutton(self, text="Preference 1", variable=self.check_value_1).pack()
        ttk.Checkbutton(self, text="Preference 2", variable=self.check_value_2).pack()

        # Text Widget
        ttk.Label(self, text="Text Box:").pack(pady=5)
        self.text_widget = tk.Text(self, height=5, width=50)
        self.text_widget.pack(pady=5)
        self.text_widget.insert("1.0", "Write something here...")

        # Listbox Widget
        ttk.Label(self, text="Listbox:").pack(pady=5)
        self.listbox_widget = tk.Listbox(self, height=5)
        self.listbox_widget.pack(pady=5)
        for item in ["Item 1", "Item 2", "Item 3"]:
            self.listbox_widget.insert(tk.END, item)

        # Scale Widget
        ttk.Label(self, text="Select a Value:").pack(pady=5)
        self.scale_widget = ttk.Scale(self, from_=0, to=100, orient="horizontal")
        self.scale_widget.pack(pady=5)

        # Progress Bar
        ttk.Label(self, text="Progress Bar:").pack(pady=5)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=5)
        ttk.Button(self, text="Start Progress", command=self.start_progress).pack(pady=5)

        # Treeview
        ttk.Label(self, text="Treeview Widget:").pack(pady=5)
        self.treeview_widget = ttk.Treeview(self, columns=("Name", "Age"), show="headings")
        self.treeview_widget.heading("Name", text="Name")
        self.treeview_widget.heading("Age", text="Age")
        self.treeview_widget.pack(pady=5)
        self.treeview_widget.insert("", tk.END, values=("John", "30"))
        self.treeview_widget.insert("", tk.END, values=("Alice", "25"))

        # File Dialog
        ttk.Button(self, text="Open File Dialog", command=self.open_file_dialog).pack(pady=10)

        # Messagebox
        ttk.Button(self, text="Show Messagebox", command=self.show_messagebox).pack(pady=10)

    # Event Handlers
    def button_clicked(self):
        text = self.entry_widget.get()
        messagebox.showinfo("Button Clicked", f"You entered: {text}")

    def start_progress(self):
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        for i in range(0, 101, 10):
            self.progress_bar["value"] = i
            self.update_idletasks()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            messagebox.showinfo("File Selected", f"You selected: {file_path}")

    def show_messagebox(self):
        messagebox.showinfo("Messagebox", "This is a sample messagebox!")

if __name__ == "__main__":
    app = TkinterWidgetsDemoApp()
    app.mainloop()
