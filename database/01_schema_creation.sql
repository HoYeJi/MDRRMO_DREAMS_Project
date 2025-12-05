-- DATABASE OVERHAUL: MDRRMO DREAMS OPERATIONS
CREATE DATABASE IF NOT EXISTS `MDRRMO_DREAMS_DB`;
USE `MDRRMO_DREAMS_DB`;

-- 1. Personnel Table (Manages Staff/Responders)
-- Personnel is linked to Incidents (as Commander) and Deployment.
CREATE TABLE Personnel (
    personnel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL, -- e.g., 'Rescuer', 'Logistics', 'Commander'
    specialty VARCHAR(50), -- e.g., 'Medical', 'Search & Rescue', 'Communications'
    contact_number VARCHAR(15),
    assigned_unit VARCHAR(50)
);

-- 2. ResponseIncidents Table (Manages Emergency Events)
-- Incident is linked to a specific Commander (Personnel) and Deployment.
CREATE TABLE ResponseIncidents (
    incident_id INT AUTO_INCREMENT PRIMARY KEY,
    incident_type VARCHAR(50) NOT NULL, -- e.g., 'Medical Emergency', 'Road Accident'
    incident_location VARCHAR(255) NOT NULL,
    date_reported DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., 'Active', 'Resolved'
    commander_id INT, -- NEW FK: The designated leader for this incident
    FOREIGN KEY (commander_id) REFERENCES Personnel(personnel_id)
);

-- 3. Resources Table (Master Inventory List)
-- Resources is linked to ResourceUsage.
CREATE TABLE Resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50), -- e.g., 'Medical Supplies', 'Vehicle', 'Equipment'
    stock_level INT NOT NULL CHECK (stock_level >= 0),
    unit_of_measure VARCHAR(20)
);

-- 4. Deployment Table (Bridge Table: Personnel <-> Incidents)
-- Tracks which personnel were actively dispatched to which incident (M:M).
CREATE TABLE Deployment (
    deployment_id INT AUTO_INCREMENT PRIMARY KEY,
    incident_id INT NOT NULL,
    personnel_id INT NOT NULL,
    deployment_time DATETIME NOT NULL,
    role_during_incident VARCHAR(50), -- Actual role assigned on site (e.g., 'Driver', 'Paramedic')
    FOREIGN KEY (incident_id) REFERENCES ResponseIncidents(incident_id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id),
    UNIQUE KEY unique_deployment (incident_id, personnel_id)
);

-- 5. ResourceUsage Table (Bridge Table: Resources <-> Incidents)
-- Tracks which resources were used for which incident (M:M).
CREATE TABLE ResourceUsage (
    usage_id INT AUTO_INCREMENT PRIMARY KEY,
    incident_id INT NOT NULL,
    resource_id INT NOT NULL,
    quantity_used INT NOT NULL,
    date_used DATETIME NOT NULL,
    FOREIGN KEY (incident_id) REFERENCES ResponseIncidents(incident_id),
    FOREIGN KEY (resource_id) REFERENCES Resources(resource_id),
    UNIQUE KEY unique_usage (incident_id, resource_id)
);