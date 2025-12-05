# 📄 Project Proposal: MDRRMO DREAMS

## I. Project Identity and Overview (Deliverable 3.1.1)

| Component | Detail |
| :--- | :--- |
| **Project Title** | **MDRRMO DREAMS** (Disaster Response and Emergency Aid Management System) |
| **Course** | IT 211 - Database Management Systems |
| **Goal** | To design and implement a functional, relational database system for a Municipal DRRM Office to manage core operational data for preparedness, response, and resource accountability. |
| **Key Technologies** | **Database:** MySQL / MariaDB (via XAMPP) <br> **GUI:** Python (using Tkinter) |

## II. Project Objectives (Deliverable 3.1.2)

The system is designed to meet the following objectives:

* **Data Modeling:** To design and implement a normalized relational database schema (3NF) consisting of 8 tables and an Entity-Relationship Diagram (ERD).
* **Application Development:** To develop a **Python (Tkinter)** Graphical User Interface (GUI) that allows authorized personnel to manage disaster-related data effectively.
* **CRUD Functionality:** To implement full **CRUD** (Create, Read, Update, Delete) capabilities across all major entities.
* **Reporting:** To generate complex SQL reports that provide meaningful insights into resource consumption, team performance, and incident frequency.

## III. Project Scope: 4 Core Focus Areas

The system's functionality is limited to managing data related to these four core operational areas of the MDRRMO, based on the Citizen's Charter:

| \# | Focus Area | Description | Core Entities Managed |
| :--- | :--- | :--- | :--- |
| **1.** | **Emergency Response Logging** | Records details of spontaneous 24/7 emergencies (e.g., Road Accidents, Medical Emergencies) and their immediate status. | `ResponseIncidents` |
| **2.** | **Scheduled Service Management** | Tracks and schedules pre-requested services from the community (e.g., Tree Trimming, Site Inspections). | `ServiceRequests`, `ServiceType` |
| **3.** | **Resource and Equipment Inventory** | Monitors the stock levels of relief goods and specialized equipment; logs usage during incidents for accountability. | `Resources`, `ResourceUsage` |
| **4.** | **Training Event Management** | Organizes and maintains records of DRRM training events, participant capacity, and attendee sign-in data. | `TrainingEvents`, `Attendees` |