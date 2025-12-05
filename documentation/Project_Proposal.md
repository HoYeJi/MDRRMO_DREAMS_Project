# 📄 Project Proposal: MDRRMO DREAMS

## 1. Project Title and Description

| Component | Detail |
| :--- | :--- |
| **Project Title** | **MDRRMO DREAMS** (Disaster Response and Emergency Aid Management System) |
| **Course** | IT 211 - Database Management Systems |
| **Description** | A streamlined database management system for the Municipal DRRM Office. The system centralizes data on **emergency incidents, personnel deployment, and resource usage**. This focused approach ensures maximum accountability and real-time tracking within the core operational pipeline, while maintaining the original DREAMS vision on a smaller, highly interconnected structure. |

---

## 2. Objectives

The system is designed to meet the following key academic and functional objectives:

* **Database Design:** To design and implement a **highly interconnected** normalized relational database schema (5 tables) that models the crucial M:M relationships between Personnel, Incidents, and Resources.
* **CRUD Functionality:** To develop a **Python (Tkinter) GUI** to implement full CRUD (Create, Read, Update, Delete) capabilities for the core entities (Personnel, Incidents, Resources).
* **Reporting:** To generate complex, multi-join SQL reports that track the efficiency of emergency response, resource accountability, and team performance.
* **Application Integration:** To successfully connect the Python application to the **MySQL/MariaDB** server.

---

## 3. Tools and Technologies

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Database Management** | **MySQL / MariaDB** | Stores all relational data (via XAMPP). |
| **Application Logic** | **Python** | Primary programming language. |
| **Graphical User Interface (GUI)** | **Tkinter** | Python's standard library used to build the desktop interface. |

---

## 4. Proposed Database Structure (5 Highly Connected Tables)

The system focuses on three core operational areas, modeled by five highly-connected entities:

| \# | Core Focus Area | Entities Managed | Key Relationships |
| :---: | :--- | :--- | :--- |
| **1.** | **Emergency Response & Deployment** | `ResponseIncidents`, `Deployment` | Incident is commanded by a Personnel (FK), and linked to multiple Personnel (M:M via Deployment). |
| **2.** | **Resource Inventory & Tracking** | `Resources`, `ResourceUsage` | Resources are tracked and linked to specific incidents where they were consumed (M:M via ResourceUsage). |
| **3.** | **Personnel Management** | `Personnel` | Staff and responders are tracked, assigned as Commanders to incidents, and tracked during field deployments. |

| Table Name | Description | Key Relationships |
| :--- | :--- | :--- |
| **1. Personnel** | Staff details, roles, and specialties. | `ResponseIncidents` (Commander FK), `Deployment` (M:M) |
| **2. ResponseIncidents** | Logs emergency events, location, status, and designated **Commander**. | `Personnel` (Commander FK), `Deployment` (M:M), `ResourceUsage` (M:M) |
| **3. Resources** | Master inventory of equipment and supplies. | `ResourceUsage` (M:M) |
| **4. Deployment** | **Bridge Table:** Tracks which `Personnel` were deployed to which `Incident`. | Links `Personnel` and `ResponseIncidents` (M:M) |
| **5. ResourceUsage** | **Bridge Table:** Tracks which `Resources` were consumed during which `Incident`. | Links `Resources` and `ResponseIncidents` (M:M) |