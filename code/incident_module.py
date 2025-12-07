import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

class IncidentModule(tk.Toplevel):
    def __init__(self, connection, master):
        super().__init__(master)
        self.conn = connection
        self.title("Incident & Deployment Management")
        self.geometry("1100x650")

        self.transient(master)
        self.grab_set()

        # Data holders for Commanders (for the dropdown)
        self.personnel_map = {}
        self.load_personnel_map()

        # --- Interface Setup ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Left Side: Input Form (CRUD - C/U)
        self.form_frame = tk.LabelFrame(main_frame, text="Log/Edit Incident")
        self.form_frame.pack(side='left', fill='y', padx=10, pady=5, ipadx=5)
        self.create_form_widgets()

        # Right Side: Data View (CRUD - R)
        self.view_frame = tk.LabelFrame(main_frame, text="Active & Resolved Incidents")
        self.view_frame.pack(side='right', fill='both', expand=True, padx=10, pady=5)
        self.create_data_view()

        self.load_incident_data()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_personnel_map(self):
        """Loads personnel names and IDs for the Commander dropdown."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT personnel_id, name FROM Personnel ORDER BY name")
            # Map of {name: id}
            self.personnel_map = {name: id for id, name in cursor.fetchall()}
        except Error as e:
            messagebox.showerror("DB Error", f"Could not load Personnel list: {e}")
        finally:
            cursor.close()

    def create_form_widgets(self):
        # Hidden ID field for editing
        self.incident_id_var = tk.StringVar()

        # 1. Incident Type
        tk.Label(self.form_frame, text="Incident Type:").pack(pady=5, padx=5, anchor='w')
        self.type_entry = tk.Entry(self.form_frame, width=30)
        self.type_entry.pack(pady=5, padx=5)

        # 2. Location
        tk.Label(self.form_frame, text="Location:").pack(pady=5, padx=5, anchor='w')
        self.location_entry = tk.Entry(self.form_frame, width=30)
        self.location_entry.pack(pady=5, padx=5)

        # 3. Date/Time Reported (Use a simple Entry for now)
        # NOTE: Using a simple entry requires the user to input the correct MySQL format (YYYY-MM-DD HH:MM:SS)
        tk.Label(self.form_frame, text="Date/Time (YYYY-MM-DD HH:MM:SS):").pack(pady=5, padx=5, anchor='w')
        self.date_entry = tk.Entry(self.form_frame, width=30)
        self.date_entry.pack(pady=5, padx=5)

        # 4. Status (Dropdown)
        tk.Label(self.form_frame, text="Status:").pack(pady=5, padx=5, anchor='w')
        self.status_var = tk.StringVar(self)
        self.status_var.set("Active")
        status_options = ["Active", "Resolved", "Standby"]
        tk.OptionMenu(self.form_frame, self.status_var, *status_options).pack(pady=5, padx=5, fill='x')

        # 5. Commander (Dropdown using loaded personnel map)
        tk.Label(self.form_frame, text="Incident Commander:").pack(pady=5, padx=5, anchor='w')
        self.commander_var = tk.StringVar(self)
        personnel_names = sorted(self.personnel_map.keys())
        if personnel_names:
            # Set default commander to the first one alphabetically
            self.commander_var.set(personnel_names[0]) 
            tk.OptionMenu(self.form_frame, self.commander_var, *personnel_names).pack(pady=5, padx=5, fill='x')
        else:
            tk.Label(self.form_frame, text="No Personnel Found").pack(pady=5, padx=5)

        # --- Action Buttons ---
        button_frame = tk.Frame(self.form_frame)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Log New Incident", command=self.add_incident).pack(side='left', padx=5)
        self.update_btn = tk.Button(button_frame, text="Update Incident", state=tk.DISABLED, command=self.update_incident)
        self.update_btn.pack(side='left', padx=5)

        tk.Button(self.form_frame, text="Clear Form", command=self.clear_form).pack(pady=5)

    def create_data_view(self):
        # --- Treeview (Data Grid) ---
        columns = ("ID", "Type", "Location", "Date Reported", "Status", "Commander")
        self.tree = ttk.Treeview(self.view_frame, columns=columns, show='headings')

        # Column Headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Date Reported", text="Date Reported")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Commander", text="Commander")

        self.tree.column("ID", width=40, anchor='center')
        self.tree.column("Type", width=120)
        self.tree.column("Location", width=250)
        self.tree.column("Date Reported", width=140)
        self.tree.column("Status", width=80, anchor='center')
        self.tree.column("Commander", width=150)

        vsb = ttk.Scrollbar(self.view_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(fill='both', expand=True)

        self.tree.bind('<<TreeviewSelect>>', self.select_incident)

        # --- Delete Button ---
        tk.Button(self.view_frame, text="Delete Selected Incident", command=self.delete_incident, bg='red', fg='white').pack(pady=10)
        
        # NOTE: Deployment management is complex and will be added later or managed via a separate button/window.

    # --- CRUD Methods ---

    def load_incident_data(self):
        """CRUD - R (READ): Loads all incidents, joining with Personnel to show the Commander's name."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        cursor = self.conn.cursor()
        try:
            # Join Incidents with Personnel (P) on commander_id to display the commander's name
            query = """
                SELECT 
                    I.incident_id, I.incident_type, I.incident_location, I.date_reported, I.status, P.name
                FROM 
                    ResponseIncidents AS I
                JOIN 
                    Personnel AS P ON I.commander_id = P.personnel_id
                ORDER BY
                    I.date_reported DESC;
            """
            cursor.execute(query)
            records = cursor.fetchall()
            
            for row in records:
                # Format the date/time to a cleaner string for the display
                row_list = list(row)
                row_list[3] = row_list[3].strftime('%Y-%m-%d %H:%M:%S')
                self.tree.insert('', tk.END, values=row_list)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load incident data: {e}")
        finally:
            cursor.close()

    def add_incident(self):
        """CRUD - C (CREATE)"""
        incident_type = self.type_entry.get()
        location = self.location_entry.get()
        date_reported = self.date_entry.get()
        status = self.status_var.get()
        commander_name = self.commander_var.get()
        # Look up the ID from the name
        commander_id = self.personnel_map.get(commander_name)
        
        if not all([incident_type, location, date_reported, status, commander_id]):
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        query = """
            INSERT INTO ResponseIncidents 
            (incident_type, incident_location, date_reported, status, commander_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (incident_type, location, date_reported, status, commander_id)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "New incident logged successfully!")
            self.load_incident_data()
            self.clear_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to log incident: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def select_incident(self, event):
        """Populates the form when a row is selected."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            
            self.clear_form(keep_selection=True) 
            
            # Use incident ID for hidden tracking
            self.incident_id_var.set(values[0])
            self.update_btn.config(state=tk.NORMAL)
            
            # Populate fields
            self.type_entry.insert(0, values[1])
            self.location_entry.insert(0, values[2])
            self.date_entry.insert(0, values[3]) # Already formatted string
            
            # Set dropdowns
            self.status_var.set(values[4])
            self.commander_var.set(values[5]) 

    def update_incident(self):
        """CRUD - U (UPDATE)"""
        incident_id = self.incident_id_var.get()
        if not incident_id:
            messagebox.showwarning("Selection Error", "No incident selected for update.")
            return

        incident_type = self.type_entry.get()
        location = self.location_entry.get()
        date_reported = self.date_entry.get()
        status = self.status_var.get()
        commander_name = self.commander_var.get()
        commander_id = self.personnel_map.get(commander_name)
        
        query = """
            UPDATE ResponseIncidents 
            SET incident_type=%s, incident_location=%s, date_reported=%s, status=%s, commander_id=%s 
            WHERE incident_id=%s
        """
        values = (incident_type, location, date_reported, status, commander_id, incident_id)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", f"Incident ID {incident_id} updated successfully!")
            self.load_incident_data()
            self.clear_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update incident: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def delete_incident(self):
        """CRUD - D (DELETE)"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an incident record to delete.")
            return

        incident_id = self.tree.item(selected_item, 'values')[0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Incident ID {incident_id}? This will also delete related Deployment and Resource Usage records (due to cascading dependencies)."):
            
            cursor = self.conn.cursor()
            try:
                # IMPORTANT: Delete related records in bridge tables first due to Foreign Keys
                # NOTE: You must disable foreign key checks or set ON DELETE CASCADE in the schema.
                # Assuming ON DELETE CASCADE is NOT set, we must delete manually:
                cursor.execute("DELETE FROM ResourceUsage WHERE incident_id = %s", (incident_id,))
                cursor.execute("DELETE FROM Deployment WHERE incident_id = %s", (incident_id,))
                
                # Now delete the main incident record
                cursor.execute("DELETE FROM ResponseIncidents WHERE incident_id = %s", (incident_id,))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Incident record and related deployments/usage deleted.")
                self.load_incident_data()
                self.clear_form()
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to delete incident: {e}")
                self.conn.rollback()
            finally:
                cursor.close()

    def clear_form(self, keep_selection=False):
        """Resets all form entries and button states."""
        self.type_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

        if not keep_selection:
            self.incident_id_var.set("")
            self.update_btn.config(state=tk.DISABLED)
        
        if self.personnel_map and not keep_selection:
            self.commander_var.set(sorted(self.personnel_map.keys())[0])
        if not keep_selection:
            self.status_var.set("Active")

        if not keep_selection:
            self.tree.selection_remove(self.tree.selection())

    def on_close(self):
        """Handles closing the Toplevel window."""
        self.grab_release()
        self.destroy()