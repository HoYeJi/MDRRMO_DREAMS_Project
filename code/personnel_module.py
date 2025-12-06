import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

class PersonnelModule(tk.Toplevel):
    def __init__(self, connection, master):
        super().__init__(master)
        self.conn = connection
        self.title("Personnel Management (CRUD)")
        self.geometry("1000x600")
        
        # Lock the main window while this one is open
        self.transient(master)
        self.grab_set()
        
        # --- Interface Setup ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Side: Input Form (CRUD - C/U)
        self.form_frame = tk.LabelFrame(main_frame, text="Add/Edit Personnel")
        self.form_frame.pack(side='left', fill='y', padx=10, pady=5, ipadx=5)
        self.create_form_widgets()
        
        # Right Side: Data View (CRUD - R)
        self.view_frame = tk.LabelFrame(main_frame, text="Personnel Records")
        self.view_frame.pack(side='right', fill='both', expand=True, padx=10, pady=5)
        self.create_data_view()

        # Load data immediately
        self.load_personnel_data()
        
        # Set protocol for closing the window cleanly
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_form_widgets(self):
        # --- Form Inputs ---
        
        # 1. Name
        tk.Label(self.form_frame, text="Name:").pack(pady=5, padx=5, anchor='w')
        self.name_entry = tk.Entry(self.form_frame, width=30)
        self.name_entry.pack(pady=5, padx=5)

        # 2. Role
        tk.Label(self.form_frame, text="Role:").pack(pady=5, padx=5, anchor='w')
        self.role_entry = tk.Entry(self.form_frame, width=30)
        self.role_entry.pack(pady=5, padx=5)
        
        # 3. Specialty (e.g., Medical, Search & Rescue)
        tk.Label(self.form_frame, text="Specialty:").pack(pady=5, padx=5, anchor='w')
        self.specialty_entry = tk.Entry(self.form_frame, width=30)
        self.specialty_entry.pack(pady=5, padx=5)
        
        # 4. Contact Number
        tk.Label(self.form_frame, text="Contact No.:").pack(pady=5, padx=5, anchor='w')
        self.contact_entry = tk.Entry(self.form_frame, width=30)
        self.contact_entry.pack(pady=5, padx=5)
        
        # 5. Assigned Unit
        tk.Label(self.form_frame, text="Assigned Unit:").pack(pady=5, padx=5, anchor='w')
        self.unit_entry = tk.Entry(self.form_frame, width=30)
        self.unit_entry.pack(pady=5, padx=5)

        # Hidden ID field for editing (Update/Delete)
        self.personnel_id_var = tk.StringVar()

        # --- Action Buttons (CREATE / UPDATE) ---
        button_frame = tk.Frame(self.form_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Add New", command=self.add_personnel).pack(side='left', padx=5)
        self.update_btn = tk.Button(button_frame, text="Update Selected", state=tk.DISABLED, command=self.update_personnel)
        self.update_btn.pack(side='left', padx=5)
        
        tk.Button(self.form_frame, text="Clear Form", command=self.clear_form).pack(pady=5)
        
    def create_data_view(self):
        # --- Treeview (Data Grid) ---
        
        # Define Columns for the Personnel table
        columns = ("ID", "Name", "Role", "Specialty", "Contact", "Unit")
        self.tree = ttk.Treeview(self.view_frame, columns=columns, show='headings')

        # Set Column Headings and Widths
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Specialty", text="Specialty")
        self.tree.heading("Contact", text="Contact No.")
        self.tree.heading("Unit", text="Unit")

        self.tree.column("ID", width=40, anchor='center')
        self.tree.column("Name", width=150)
        self.tree.column("Role", width=100)
        self.tree.column("Specialty", width=100)
        self.tree.column("Contact", width=120)
        self.tree.column("Unit", width=100)

        # Scrollbar
        vsb = ttk.Scrollbar(self.view_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind event: When a row is selected, populate the form for editing
        self.tree.bind('<<TreeviewSelect>>', self.select_personnel)

        # --- Delete Button (CRUD - D) ---
        tk.Button(self.view_frame, text="Delete Selected", command=self.delete_personnel, bg='red', fg='white').pack(pady=10)

    # --- CRUD Methods ---

    def load_personnel_data(self):
        """CRUD - R (READ)"""
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        cursor = self.conn.cursor()
        try:
            # Query to fetch all personnel data
            cursor.execute("SELECT personnel_id, name, role, specialty, contact_number, assigned_unit FROM Personnel")
            records = cursor.fetchall()
            
            # Insert data into the Treeview
            for row in records:
                self.tree.insert('', tk.END, values=row)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load personnel data: {e}")
        finally:
            cursor.close()

    def add_personnel(self):
        """CRUD - C (CREATE)"""
        name = self.name_entry.get()
        role = self.role_entry.get()
        specialty = self.specialty_entry.get()
        contact = self.contact_entry.get()
        unit = self.unit_entry.get()
        
        # Basic validation
        if not all([name, role, contact, unit]):
            messagebox.showwarning("Input Error", "All fields except Specialty must be filled.")
            return

        query = "INSERT INTO Personnel (name, role, specialty, contact_number, assigned_unit) VALUES (%s, %s, %s, %s, %s)"
        values = (name, role, specialty, contact, unit)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "New personnel added successfully!")
            self.load_personnel_data() # Refresh table
            self.clear_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to add personnel: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def select_personnel(self, event):
        """Populates the form when a row in the Treeview is selected."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            
            self.clear_form(keep_id=True) # Clear and prepare form
            
            # Set hidden ID and enable Update/Delete buttons
            self.personnel_id_var.set(values[0])
            self.update_btn.config(state=tk.NORMAL)
            
            # Populate fields
            self.name_entry.insert(0, values[1])
            self.role_entry.insert(0, values[2])
            self.specialty_entry.insert(0, values[3])
            self.contact_entry.insert(0, values[4])
            self.unit_entry.insert(0, values[5])

    def update_personnel(self):
        """CRUD - U (UPDATE)"""
        personnel_id = self.personnel_id_var.get()
        if not personnel_id:
            messagebox.showwarning("Selection Error", "No personnel selected for update.")
            return

        name = self.name_entry.get()
        role = self.role_entry.get()
        specialty = self.specialty_entry.get()
        contact = self.contact_entry.get()
        unit = self.unit_entry.get()
        
        query = "UPDATE Personnel SET name=%s, role=%s, specialty=%s, contact_number=%s, assigned_unit=%s WHERE personnel_id=%s"
        values = (name, role, specialty, contact, unit, personnel_id)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", f"Personnel ID {personnel_id} updated successfully!")
            self.load_personnel_data()
            self.clear_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update personnel: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def delete_personnel(self):
        """CRUD - D (DELETE)"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a personnel record to delete.")
            return

        personnel_id = self.tree.item(selected_item, 'values')[0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Personnel ID {personnel_id}?"):
            query = "DELETE FROM Personnel WHERE personnel_id = %s"
            cursor = self.conn.cursor()
            try:
                # Note: Deleting personnel might violate FK constraints in ResponseIncidents (commander_id) or Deployment. 
                # For this project, assume personnel must not be deleted if they commanded an incident.
                cursor.execute(query, (personnel_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Personnel record deleted.")
                self.load_personnel_data()
                self.clear_form()
            except Error as e:
                if e.errno == 1451: # MySQL error for Foreign Key constraint
                    messagebox.showerror("Constraint Error", f"Cannot delete Personnel ID {personnel_id}. They are linked as a Commander or deployed to an active incident.")
                else:
                    messagebox.showerror("Database Error", f"Failed to delete personnel: {e}")
                self.conn.rollback()
            finally:
                cursor.close()

    def clear_form(self, keep_id=False):
        """Resets all form entries and button states."""
        self.name_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.specialty_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.update_btn.config(state=tk.DISABLED)
        self.tree.selection_remove(self.tree.selection())

    def on_close(self):
        """Handles closing the Toplevel window."""
        self.grab_release()
        self.destroy()