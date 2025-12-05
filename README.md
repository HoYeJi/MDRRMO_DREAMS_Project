# 📊 MDRRMO DREAMS: Disaster Response and Emergency Aid Management System (Core Operations Focus)

## Project Overview

**MDRRMO DREAMS** is a **focused** Database Management System for the Municipal Disaster Risk Reduction and Management Office (MDRRMO). The system is built on a highly interconnected 5-table schema designed to manage the critical operational pipeline: **Emergency Incidents, Personnel Deployment, and Resource Accountability.**

---

## 🎯 Key Focus Areas (Scope)

The application provides full CRUD (Create, Read, Update, Delete) functionality across **3 core, highly-connected operational areas:**

1.  **Emergency Response Logging:** Tracks all spontaneous 24/7 incidents and the designated Incident Commander.
2.  **Resource Inventory & Tracking:** Monitors stock levels of equipment and supplies, and tracks their consumption per incident using a bridge table (`ResourceUsage`).
3.  **Personnel Management & Deployment:** Tracks staff details, specialties, and uses a bridge table (`Deployment`) to log which personnel were assigned to which incident.

---

## 🛠️ Technology Stack

| Component | Technology | Version / Notes |
| :--- | :--- | :--- |
| **Database Management System** | **MySQL / MariaDB** | Executed via XAMPP |
| **Backend / Application Logic** | **Python** | Python 3.13.3 |
| **Graphical User Interface (GUI)** | **Tkinter** | Standard Python library |

---

## 📁 Repository Structure

* **`CODE/`**: Contains all Python source files (`.py`) for the GUI, database connection, and application logic.
* **`DATABASE/`**: Stores all SQL scripts for schema creation and sample data population.
* **`DOCUMENTATION/`**: Contains planning documents, including the official project proposal.
* **`REPORTS/`**: Holds final deliverables, including the ERD image and the final academic report.

---

## ⚙️ Setup and Execution Guide

### 1. Database Setup

1.  Start the **Apache** and **MySQL** services in XAMPP.
2.  Open **phpMyAdmin** in your browser.
3.  **Import** the following scripts in order to create and populate the database:
    * `DATABASE/01_schema_creation.sql` (Creates the 5-table structure)
    * `DATABASE/02_sample_data.sql` (Populates the tables with test data)

### 2. Application Setup

1.  Install necessary Python database connectors (e.g., `pip install mysql-connector-python`).
2.  Run the main application file: `python CODE/main_app.py`

---