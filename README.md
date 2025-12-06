# 📊 MDRRMO DREAMS: Disaster Response and Emergency Aid Management System (Core Operations Focus)

## 1. Project Overview & Objectives (Deliverables 3.1.1, 3.1.2)

The **MDRRMO DREAMS** (Disaster Response and Emergency Aid Management System) is a comprehensive database application designed for a Municipal Disaster Risk Reduction and Management Office. Its purpose is to streamline core emergency operations, deployment logistics, and inventory tracking.

This project was developed to meet the following objectives of the IT 211 course:

* **Demonstrate understanding of database concepts and design.** (1.1)
* **Apply knowledge of SQL, CRUD operations, and relational databases.** (1.2)
* **Develop a functional system with a user-friendly interface** to manage personnel, incidents, and resources. (1.3, 2.3)
* **Generate complex reports and queries** to retrieve meaningful analytical data on disaster response performance and resource consumption. (2.5)

***

## 2. Project Scope & Architecture (Deliverables 3.1.3, 3.4.2)

### 🛠️ Tools and Technologies

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Database** | **MySQL (via XAMPP)** | Stores all operational and inventory data. |
| **Database Connector** | **`mysql-connector-python`** | Facilitates communication between Python and MySQL. |
| **Application GUI** | **Python (Tkinter)** | Provides the user interface for data interaction and management. |
| **Language** | **SQL, Python** | Used for data definition/manipulation and application logic. |

### 🚀 System Architecture

The system utilizes a **Two-Tier Architecture**: the **Python/Tkinter GUI client** connects directly to the local **MySQL server** (hosted on XAMPP). This connection is managed through the central `db_connector.py` module. 

***

## 3. Database Design and Implementation (Deliverables 3.2, 3.4.1)

The system is built upon a **5-table, highly normalized relational schema** focused on operational integrity and minimal redundancy (3.2.3).

### 📊 Schema and Relationships (3.2.2)

The database, named `MDRRMO_DREAMS_DB`, consists of three core entity tables and two many-to-many (M:M) bridge tables:

| Table Name | Purpose | Key Relationships |
| :--- | :--- | :--- |
| **`Personnel`** | Master list of all MDRRMO staff and responders. | One-to-Many (`1:M`) to `ResponseIncidents` (Commander). |
| **`Resources`** | Master inventory list of all equipment and supplies. | One-to-Many (`1:M`) to `ResourceUsage`. |
| **`ResponseIncidents`** | Logs of all emergency events. | One-to-Many (`1:M`) to `Deployment` and `ResourceUsage`. |
| **`Deployment`** | **M:M Bridge** linking `Personnel` to `ResponseIncidents`. | Tracks which specific personnel were deployed to which incident. |
| **`ResourceUsage`** | **M:M Bridge** linking `Resources` to `ResponseIncidents`. | Tracks the quantity of resources consumed during an incident. |

### 📁 Database Scripts

The entire database can be deployed using the following scripts located in the `DATABASE/` folder:

1.  `01_schema_creation.sql`: Creates the `MDRRMO_DREAMS_DB` and all 5 tables with primary and foreign keys.
2.  `02_sample_data.sql`: Populates the tables with interconnected sample records for testing.
3.  `03_reporting_queries.sql`: Contains the 5 complex SQL joins used by the Reporting Module.

***

## 4. Application Functionality (Deliverables 3.3, 3.4.3)

The Python application is split into four main modules, all implementing **CRUD operations** (2.4) and following **user-centered design principles** (2.6).

### 1. Personnel Management
* **CRUD:** Full functionality for adding, editing, viewing, and deleting staff records.

### 2. Incident & Deployment Management
* **CRUD:** Allows logging new incidents and updating status/details.
* **Interconnectivity:** Uses a dropdown list populated by the **`Personnel`** table to assign an Incident Commander (`commander_id`).

### 3. Resources & Inventory
* **Resources CRUD:** Manages the master inventory list (item details, categories, units).
* **Usage Logic (Bridge Table):** Allows logging resource consumption against an **Incident**. This operation automatically **updates (decrements)** the `stock_level` in the **`Resources`** table, demonstrating functional data integrity.

### 4. Reporting & Analytics (2.5)
The Reports Module displays results from **5 complex analytical queries** using the Treeview widget across dedicated tabs:
1.  **Incident Performance:** Shows the Commander and total number of personnel deployed per incident.
2.  **Personnel Utilization:** Logs all personnel deployments, their specialty, and their role on site.
3.  **Resource Consumption Detail:** Lists the exact quantity of items consumed per incident.
4.  **Low-Stock Inventory Alert:** Filters for resources with stock levels $\le 5$.
5.  **Incidents Lacking Resource Logs:** Identifies potential auditing gaps.

***

## 5. Setup and Execution Guide (Deliverable 3.5.1)

### Prerequisites

1.  **XAMPP:** Must be installed and running (Apache and MySQL services started).
2.  **Python 3.13.3:** Must be installed.
3.  **Dependencies:** Install the MySQL connector: `pip install mysql-connector-python`

### Database Setup

1.  Open **phpMyAdmin** (`http://localhost/phpmyadmin`).
2.  Import the **`DATABASE/01_schema_creation.sql`** script to create the database structure.
3.  Select the `MDRRMO_DREAMS_DB` and import the **`DATABASE/02_sample_data.sql`** script to populate the tables.

### Application Launch

1.  Ensure **XAMPP MySQL is running**.
2.  Open your terminal in the project's root directory.
3.  Run the main application file:
    ```bash
    python CODE/main_app.py
    ```

The application will launch, connect to the database, and is ready for use.