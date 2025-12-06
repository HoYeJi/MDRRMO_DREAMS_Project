import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

class ResourceModule(tk.Toplevel):
    def __init__(self, connection, master):
        super().__init__(master)
        self.conn = connection
        self.title("Resources & Inventory Management")
        self.geometry("1200x650")

        self.transient(master)
        self.grab_set()

        # Data holders
        self.resource_map = {} # Maps item_name to resource_id

        # --- Interface Setup ---
        main_pane = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill='both', expand=True, padx=10, pady=10)

        # 1. Left Frame: Resources Master CRUD (List & Form)
        master_frame = tk.Frame(main_pane)
        main_pane.add(master_frame, weight=3)
        self.create_master_crud_widgets(master_frame)

        # 2. Right Frame: Resource Usage Log
        usage_frame = tk.Frame(main_pane)
        main_pane.add(usage_frame, weight=2)
        self.create_usage_log_widgets(usage_frame)

        self.load_resource_data()
        self.load_incident_list()
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    # --- Master CRUD Panel (Left Side) ---

    def create_master_crud_widgets(self, master_frame):
        # Top half: Form
        self.master_form_frame = tk.LabelFrame(master_frame, text="Add/Edit Resource Inventory")
        self.master_form_frame.pack(fill='x', padx=5, pady=5)
        
        # Form Inputs
        self.resource_id_var = tk.StringVar()
        inputs = [
            ("Item Name:", "name_entry"),
            ("Category:", "category_entry"),
            ("Stock Level:", "stock_entry"),
            ("Unit:", "unit_entry")
        ]
        
        for text, attr in inputs:
            tk.Label(self.master_form_frame, text=text, anchor='w').pack(pady=2, padx=5, fill='x')
            setattr(self, attr, tk.Entry(self.master_form_frame, width=30))
            getattr(self, attr).pack(pady=2, padx=5, fill='x')
        
        # Buttons
        button_frame = tk.Frame(self.master_form_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add New Item", command=self.add_resource).pack(side='left', padx=5)
        self.update_master_btn = tk.Button(button_frame, text="Update Item", state=tk.DISABLED, command=self.update_resource)
        self.update_master_btn.pack(side='left', padx=5)
        tk.Button(self.master_form_frame, text="Clear Form", command=self.clear_master_form).pack(pady=5)


        # Bottom half: Data View
        self.master_view_frame = tk.LabelFrame(master_frame, text="Current Inventory")
        self.master_view_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ("ID", "Item Name", "Category", "Stock", "Unit")
        self.master_tree = ttk.Treeview(self.master_view_frame, columns=columns, show='headings')
        for col in columns:
            self.master_tree.heading(col, text=col)
        self.master_tree.column("ID", width=40, anchor='center')
        self.master_tree.column("Stock", width=60, anchor='center')
        
        vsb = ttk.Scrollbar(self.master_view_frame, orient="vertical", command=self.master_tree.yview)
        vsb.pack(side='right', fill='y')
        self.master_tree.configure(yscrollcommand=vsb.set)
        self.master_tree.pack(fill='both', expand=True)

        self.master_tree.bind('<<TreeviewSelect>>', self.select_resource)
        tk.Button(self.master_view_frame, text="Delete Selected Item", command=self.delete_resource, bg='red', fg='white').pack(pady=5)


    # --- Resource Usage Log Panel (Right Side) ---

    def create_usage_log_widgets(self, usage_frame):
        # Incident Selection (Dropdown)
        incident_label = tk.Label(usage_frame, text="Log Usage Against Incident:", font=('Arial', 12, 'bold'))
        incident_label.pack(pady=10)
        
        self.incident_var = tk.StringVar(self)
        self.incident_options = []
        self.incident_dropdown = tk.OptionMenu(usage_frame, self.incident_var, "")
        self.incident_dropdown.pack(pady=5, padx=10, fill='x')
        
        # Resource Selection (Dropdown, updated dynamically)
        resource_label = tk.Label(usage_frame, text="Resource Consumed:", font=('Arial', 10))
        resource_label.pack(pady=5)
        self.usage_resource_var = tk.StringVar(self)
        self.usage_resource_var.set("Select Resource")
        self.resource_dropdown = tk.OptionMenu(usage_frame, self.usage_resource_var, "")
        self.resource_dropdown.pack(pady=5, padx=10, fill='x')
        
        # Quantity Used
        tk.Label(usage_frame, text="Quantity Used:").pack(pady=5)
        self.quantity_entry = tk.Entry(usage_frame, width=20)
        self.quantity_entry.pack(pady=5)

        # Log Button
        tk.Button(usage_frame, text="LOG RESOURCE USAGE", command=self.log_resource_usage, bg='blue', fg='white').pack(pady=20, padx=10, fill='x')

        # Usage History View (To see what was logged)
        tk.Label(usage_frame, text="Resource Usage History", font=('Arial', 10, 'underline')).pack(pady=10)
        self.usage_tree = ttk.Treeview(usage_frame, columns=("ID", "Incident", "Resource", "Quantity"), show='headings', height=10)
        self.usage_tree.heading("ID", text="ID")
        self.usage_tree.heading("Incident", text="Incident ID")
        self.usage_tree.heading("Resource", text="Resource")
        self.usage_tree.heading("Quantity", text="Qty Used")
        self.usage_tree.column("ID", width=40)
        self.usage_tree.column("Incident", width=80)
        self.usage_tree.pack(fill='x', padx=10)
        self.load_usage_history()


    # --- Utility/Data Load Methods ---

    def load_resource_data(self):
        """CRUD - R (READ) for Resources master list."""
        for item in self.master_tree.get_children():
            self.master_tree.delete(item)
            
        self.resource_map = {}
        resource_names = []
            
        cursor = self.conn.cursor()
        try:
            query = "SELECT resource_id, item_name, category, stock_level, unit_of_measure FROM Resources ORDER BY item_name"
            cursor.execute(query)
            records = cursor.fetchall()
            
            for row in records:
                self.master_tree.insert('', tk.END, values=row)
                self.resource_map[row[1]] = row[0] # Map Name -> ID
                resource_names.append(row[1])
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load resource data: {e}")
        finally:
            cursor.close()
            
        # Update the usage dropdown list
        self.update_resource_dropdown(resource_names)

    def load_incident_list(self):
        """Loads Active/Resolved incidents for the Usage dropdown."""
        cursor = self.conn.cursor()
        try:
            # Show ID and Type for easy identification
            cursor.execute("SELECT incident_id, incident_type FROM ResponseIncidents ORDER BY incident_id DESC")
            records = cursor.fetchall()
            
            self.incident_options = [f"ID {id}: {type}" for id, type in records]
            if not self.incident_options:
                self.incident_options = ["(No Incidents Logged)"]

            # Update OptionMenu options
            menu = self.incident_dropdown["menu"]
            menu.delete(0, "end")
            for option in self.incident_options:
                menu.add_command(label=option, command=lambda value=option: self.incident_var.set(value))
            
            self.incident_var.set(self.incident_options[0])

        except Error as e:
            messagebox.showerror("DB Error", f"Could not load Incident list: {e}")
        finally:
            cursor.close()
            
    def load_usage_history(self):
        """Loads the history of resource usage for the right panel."""
        for item in self.usage_tree.get_children():
            self.usage_tree.delete(item)
            
        cursor = self.conn.cursor()
        try:
            # Join ResourceUsage (RU) with Resources (R) and Incidents (I)
            query = """
                SELECT 
                    RU.usage_id, I.incident_id, R.item_name, RU.quantity_used
                FROM 
                    ResourceUsage AS RU
                JOIN 
                    ResponseIncidents AS I ON RU.incident_id = I.incident_id
                JOIN
                    Resources AS R ON RU.resource_id = R.resource_id
                ORDER BY
                    RU.usage_id DESC LIMIT 10;
            """
            cursor.execute(query)
            records = cursor.fetchall()
            
            for row in records:
                self.usage_tree.insert('', tk.END, values=row)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load usage history: {e}")
        finally:
            cursor.close()

    def update_resource_dropdown(self, resource_names):
        """Refreshes the Resource Selection dropdown."""
        menu = self.resource_dropdown["menu"]
        menu.delete(0, "end")
        if not resource_names:
            resource_names = ["(No Resources)"]
        
        for option in resource_names:
            menu.add_command(label=option, command=lambda value=option: self.usage_resource_var.set(value))
        
        self.usage_resource_var.set(resource_names[0])


    # --- Master List CRUD Functions ---

    def add_resource(self):
        """CRUD - C (CREATE) for Resources."""
        name = self.name_entry.get()
        category = self.category_entry.get()
        stock = self.stock_entry.get()
        unit = self.unit_entry.get()
        
        if not all([name, category, stock, unit]):
            messagebox.showwarning("Input Error", "All fields must be filled for the Master List.")
            return

        query = "INSERT INTO Resources (item_name, category, stock_level, unit_of_measure) VALUES (%s, %s, %s, %s)"
        values = (name, category, stock, unit)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "New resource added to inventory.")
            self.load_resource_data()
            self.clear_master_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to add resource: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def select_resource(self, event):
        """Populates the form when a row in the Master Treeview is selected."""
        selected_item = self.master_tree.selection()
        if selected_item:
            values = self.master_tree.item(selected_item, 'values')
            
            self.clear_master_form(keep_id=True)
            
            self.resource_id_var.set(values[0])
            self.update_master_btn.config(state=tk.NORMAL)
            
            self.name_entry.insert(0, values[1])
            self.category_entry.insert(0, values[2])
            self.stock_entry.delete(0, tk.END) # Delete first since stock is a number
            self.stock_entry.insert(0, values[3])
            self.unit_entry.insert(0, values[4])

    def update_resource(self):
        """CRUD - U (UPDATE) for Resources."""
        resource_id = self.resource_id_var.get()
        if not resource_id:
            messagebox.showwarning("Selection Error", "No resource selected for update.")
            return

        name = self.name_entry.get()
        category = self.category_entry.get()
        stock = self.stock_entry.get()
        unit = self.unit_entry.get()
        
        query = "UPDATE Resources SET item_name=%s, category=%s, stock_level=%s, unit_of_measure=%s WHERE resource_id=%s"
        values = (name, category, stock, unit, resource_id)
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", f"Resource ID {resource_id} updated successfully!")
            self.load_resource_data()
            self.clear_master_form()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to update resource: {e}")
            self.conn.rollback()
        finally:
            cursor.close()
            
    def delete_resource(self):
        """CRUD - D (DELETE) for Resources."""
        selected_item = self.master_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a resource record to delete.")
            return

        resource_id = self.master_tree.item(selected_item, 'values')[0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Resource ID {resource_id}?"):
            query = "DELETE FROM Resources WHERE resource_id = %s"
            cursor = self.conn.cursor()
            try:
                # Deletion might fail if ResourceUsage records exist. 
                # Assuming ON DELETE CASCADE is NOT set, you must manually delete usages first.
                cursor.execute("DELETE FROM ResourceUsage WHERE resource_id = %s", (resource_id,))
                
                # Now delete the resource
                cursor.execute(query, (resource_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Resource record deleted.")
                self.load_resource_data()
                self.clear_master_form()
            except Error as e:
                if e.errno == 1451:
                    messagebox.showerror("Constraint Error", f"Cannot delete Resource ID {resource_id}. It is still tracked in ResourceUsage.")
                else:
                    messagebox.showerror("Database Error", f"Failed to delete resource: {e}")
                self.conn.rollback()
            finally:
                cursor.close()

    def clear_master_form(self, keep_id=False):
        """Resets all master form entries and button states."""
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.update_master_btn.config(state=tk.DISABLED)
        self.master_tree.selection_remove(self.master_tree.selection())


    # --- Usage Log Function ---

    def log_resource_usage(self):
        """Inserts a record into ResourceUsage and updates the stock level."""
        incident_selection = self.incident_var.get()
        resource_name = self.usage_resource_var.get()
        quantity_str = self.quantity_entry.get()

        if not incident_selection or resource_name == "Select Resource" or not quantity_str.isdigit():
            messagebox.showwarning("Input Error", "Please select an incident, a resource, and enter a valid quantity.")
            return

        try:
            quantity_used = int(quantity_str)
            resource_id = self.resource_map.get(resource_name)
            # Incident ID is extracted from the string "ID X: Type..."
            incident_id = int(incident_selection.split(':')[0].replace('ID ', '')) 
        except Exception:
            messagebox.showwarning("Error", "Invalid input format.")
            return

        cursor = self.conn.cursor()
        try:
            # 1. Get current stock
            cursor.execute("SELECT stock_level FROM Resources WHERE resource_id = %s", (resource_id,))
            current_stock = cursor.fetchone()[0]
            
            if quantity_used > current_stock:
                messagebox.showwarning("Stock Warning", f"Usage denied. Only {current_stock} units of {resource_name} remaining.")
                return

            # 2. Log usage (INSERT into ResourceUsage)
            usage_query = "INSERT INTO ResourceUsage (incident_id, resource_id, quantity_used, date_used) VALUES (%s, %s, %s, NOW())"
            cursor.execute(usage_query, (incident_id, resource_id, quantity_used))
            
            # 3. Update stock (UPDATE Resources)
            new_stock = current_stock - quantity_used
            stock_query = "UPDATE Resources SET stock_level = %s WHERE resource_id = %s"
            cursor.execute(stock_query, (new_stock, resource_id))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"{quantity_used} units of {resource_name} logged for Incident ID {incident_id}. New stock: {new_stock}.")
            
            # Refresh data views
            self.load_resource_data() # To show updated stock
            self.load_usage_history() # To show new log entry
            self.quantity_entry.delete(0, tk.END)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to log resource usage: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

    def on_close(self):
        """Handles closing the Toplevel window."""
        self.grab_release()
        self.destroy()