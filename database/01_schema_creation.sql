-- DATABASE CREATION
CREATE DATABASE IF NOT EXISTS `MDRRMO_DREAMS_DB`;
USE `MDRRMO_DREAMS_DB`;

-- 1. Personnel Table (Focus Area 5)
CREATE TABLE Personnel (
    personnel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15),
    assigned_unit VARCHAR(50)
);

-- 2. ServiceType Table
CREATE TABLE ServiceType (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- 3. ServiceRequests Table
CREATE TABLE ServiceRequests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    type_id INT NOT NULL,
    requester_name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    request_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    personnel_id INT,
    FOREIGN KEY (type_id) REFERENCES ServiceType(type_id),
    FOREIGN KEY (personnel_id) REFERENCES Personnel(personnel_id)
);

-- 4. ResponseIncidents Table
CREATE TABLE ResponseIncidents (
    incident_id INT AUTO_INCREMENT PRIMARY KEY,
    incident_type VARCHAR(50) NOT NULL,
    incident_location VARCHAR (255) NOT NULL,
    date_reported DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    reporting_person VARCHAR(100)
);

-- 5. Resources Table
CREATE TABLE Resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    stock_level INT NOT NULL CHECK (stock_level >= 0),
    unit_of_measure VARCHAR(20)
);

-- 6. ResourceUsage Table
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

-- 7. TrainingEvents Table
CREATE TABLE TrainingEvents (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_location VARCHAR(100),
    max_participants INT
);

-- 8. Attendees Table
CREATE TABLE Attendees (
    attendee_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    organization VARCHAR(100),
    contact VARCHAR(50),
    FOREIGN KEY (event_id) REFERENCES TrainingEvents(event_id)
);