import tkinter as tk
from tkinter import messagebox
from db_connector import create_connection, close_connection
from personnel_module import PersonnelModule

class DreamsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MDRRMO DREAMS - Core Operations")
        self.geometry("800x600")

        # Attempt to connect to the database
        self.conn = create_connection()
        if not self.conn:
            messagebox.showerror("Database Error", "Failed to connect to the database. Check XAMPP and db_connector.py.")
            self.destroy() # Close the app if connection fails
            return

        self.create_widgets()

    def open_personnel_module(self):
        """Opens the Personnel Management window."""
        PersonnelModule(self.conn, self)

    def create_widgets(self):
        # Placeholder for the main navigation area
        title_label = tk.Label(self, text="MDRRMO DREAMS", font=("Arial", 16))
        title_label.pack(pady=20)

        # Main Navigation Frame (Placeholder buttons for the 3 focus areas)
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        # 1. Personnel Management
        tk.Button(nav_frame, text="Personnel Management", width=25,command=self.open_personnel_module).pack(pady=5)

        # 2. Incident & Deployment Management
        tk.Button(nav_frame, text="Incident & Deployment", width=25).pack(pady=5)

        # 3. Resources & Inventory
        tk.Button(nav_frame, text="Resources & Inventory", width=25).pack(pady=5)

        # 4. Reports Module (Queries)
        tk.Button(nav_frame, text="Generate Reports", width=25).pack(pady=15)

    def on_closing(self):
        """Cleanly closes the DB connection when the app is shut down."""
        if self.conn:
            close_connection(self.conn)
        self.destroy()

if __name__ == "__main__":
    app = DreamsApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()