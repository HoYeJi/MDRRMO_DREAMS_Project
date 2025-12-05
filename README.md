# 📊 MDRRMO DREAMS: Disaster Response and Emergency Aid Management System

## Project Overview

**MDRRMO DREAMS** is a Database Management System developed for the Municipal Disaster Risk Reduction and Management Office (MDRRMO). This system centralizes and manages critical operational data derived from the official Citizen's Charter, ensuring efficiency in preparedness, response, and resource accountability.

---

## 🎯 Key Focus Areas (Scope)

The application provides full CRUD (Create, Read, Update, Delete) functionality across 4 core operational areas:

1.  **Emergency Response Logging:** Tracks all spontaneous 24/7 incidents (Medical, Road Accident) and the response status.
2.  **Scheduled Service Management:** Manages pre-requested services from the community (e.g., Tree Trimming, Site Inspections).
3.  **Resource and Equipment Inventory:** Monitors stock levels, categorization, and usage of all physical assets (vehicles, supplies, relief goods).
4.  **Training Event Management:** Maintains comprehensive records of all DRRM training events and attendee participation.

---

## 🛠️ Technology Stack

| Component | Technology | Version / Notes |
| :--- | :--- | :--- |
| **Database Management System** | **MySQL / MariaDB** | Executed via XAMPP |
| **Backend / Application Logic** | **Python** | Python 3.x |
| **Graphical User Interface (GUI)** | **Tkinter** | Standard Python library |
| **Code Editor** | **VS Code** | Used for development and Git integration |

---

## 📁 Repository Structure

The project is organized into the following directories:

* **`CODE/`**: Contains all Python source files (`.py`) for the GUI, database connection, and application logic.
* **`DATABASE/`**: Stores all SQL scripts for schema creation and sample data population.
* **`DOCUMENTATION/`**: Contains planning documents, including the official project proposal and user manuals.
* **`REPORTS/`**: Holds final deliverables, including the ERD image and the final academic report.

---

## ⚙️ Setup and Execution Guide

### 1. Database Setup

To run the application, you must first deploy the database using XAMPP:

1.  Start the **Apache** and **MySQL** services in your XAMPP Control Panel.
2.  Open **phpMyAdmin** in your browser.
3.  **Import** the following scripts in order to create and populate the database:
    * `DATABASE/01_schema_creation.sql`
    * `DATABASE/02_sample_data.sql`

### 2. Application Setup

1.  (Optional but Recommended) Create a virtual environment: `python -m venv venv`
2.  Activate the environment.
3.  Install necessary Python database connectors (e.g., `pip install mysql-connector-python`).
4.  Run the main application file: `python CODE/main_app.py`

---

## 🔑 Database Schema Reference

The system utilizes 8 normalized tables with clear relationships (see the `DATABASE/01_schema_creation.sql` file for full details):

1.  `Personnel`
2.  `ServiceType`
3.  `ServiceRequests`
4.  `ResponseIncidents`
5.  `Resources`
6.  `ResourceUsage` (Bridge Table)
7.  `TrainingEvents`
8.  `Attendees`

---
***