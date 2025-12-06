import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

class ReportModule(tk.Toplevel):
    def __init__(self, connection, master):
        super().__init__(master)
        self.conn = connection
        self.title("DREAMS Reporting & Analytics")
        self.geometry("1200x700")

        self.transient(master)
        self.grab_set()

        # Define the queries you saved in 03_reporting_queries.sql
        self.reports = {
            "Incident Performance": {
                "query": """
                    SELECT
                        I.incident_id, I.incident_type, P_Commander.name AS Commander, I.date_reported, 
                        COUNT(D.personnel_id) AS Personnel_Deployed
                    FROM ResponseIncidents AS I
                    JOIN Personnel AS P_Commander ON I.commander_id = P_Commander.personnel_id
                    LEFT JOIN Deployment AS D ON I.incident_id = D.incident_id
                    GROUP BY I.incident_id, I.incident_type, P_Commander.name, I.date_reported
                    ORDER BY I.date_reported DESC;
                """,
                "columns": ["ID", "Incident Type", "Commander", "Date Reported", "Deployed Count"]
            },
            "Personnel Utilization": {
                "query": """
                    SELECT
                        P.name, P.specialty, I.incident_type, D.deployment_time, D.role_during_incident
                    FROM Deployment AS D
                    JOIN Personnel AS P ON D.personnel_id = P.personnel_id
                    JOIN ResponseIncidents AS I ON D.incident_id = I.incident_id
                    ORDER BY D.deployment_time DESC;
                """,
                "columns": ["Personnel Name", "Specialty", "Incident Type", "Deployment Time", "Role"]
            },
            "Resource Consumption Detail": {
                "query": """
                    SELECT
                        I.incident_id, I.incident_location, R.item_name, RU.quantity_used, R.unit_of_measure
                    FROM ResourceUsage AS RU
                    JOIN ResponseIncidents AS I ON RU.incident_id = I.incident_id
                    JOIN Resources AS R ON RU.resource_id = R.resource_id
                    ORDER BY I.incident_id, R.item_name;
                """,
                "columns": ["Incident ID", "Location", "Resource", "Quantity Used", "Unit"]
            },
            "Low-Stock Inventory Alert": {
                "query": """
                    SELECT item_name, category, stock_level, unit_of_measure
                    FROM Resources
                    WHERE stock_level <= 5
                    ORDER BY stock_level ASC;
                """,
                "columns": ["Item Name", "Category", "Stock Level", "Unit"]
            },
            "Incidents Lacking Resource Logs": {
                "query": """
                    SELECT I.incident_id, I.incident_type, I.date_reported, I.commander_id
                    FROM ResponseIncidents AS I
                    LEFT JOIN ResourceUsage AS RU ON I.incident_id = RU.incident_id
                    WHERE RU.usage_id IS NULL;
                """,
                "columns": ["Incident ID", "Incident Type", "Date Reported", "Commander ID"]
            }
        }

        # --- Main Layout ---
        tk.Label(self, text="DREAMS Analytical Reports", font=("Arial", 16, 'bold')).pack(pady=10)
        
        # Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)

        self.create_report_tabs()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_report_tabs(self):
        """Creates a tab for each defined report."""
        for name, data in self.reports.items():
            frame = ttk.Frame(self.notebook, padding="10")
            self.notebook.add(frame, text=name)
            self.create_report_view(frame, name, data['query'], data['columns'])

    def create_report_view(self, parent_frame, report_name, query, columns):
        """Builds the Treeview and loads data for a specific report."""
        
        # Label/Title
        tk.Label(parent_frame, text=report_name, font=("Arial", 12, 'underline')).pack(pady=5)

        # Treeview Setup
        tree = ttk.Treeview(parent_frame, columns=columns, show='headings')
        
        # Scrollbars
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='w', width=150) # Set default width

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill='both', expand=True)

        # Load Data
        self.load_report_data(tree, query)
        
    def load_report_data(self, tree_widget, query):
        """Executes a SQL query and populates the given Treeview widget."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            records = cursor.fetchall()

            if not records:
                tree_widget.insert('', tk.END, values=("(No Data Available)",) * len(tree_widget["columns"]))
                return

            for row in records:
                # Format datetime objects for display
                formatted_row = []
                for item in row:
                    if hasattr(item, 'strftime'): # Check if it's a datetime object
                        formatted_row.append(item.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        formatted_row.append(item)
                        
                tree_widget.insert('', tk.END, values=tuple(formatted_row))

        except Error as e:
            messagebox.showerror("Report Generation Error", f"Failed to execute report query: {e}")
        finally:
            cursor.close()

    def on_close(self):
        """Handles closing the Toplevel window."""
        self.grab_release()
        self.destroy()