-- -----------------------------------------------------
-- INSERT SAMPLE DATA FOR MDRRMO DREAMS (5 TABLES)
-- This script populates the 5 highly interconnected tables
-- focusing on core emergency operations, deployment, and resources.
-- -----------------------------------------------------

-- Ensure the correct database is selected before inserting data
USE `MDRRMO_DREAMS_DB`;

-- 1. Personnel (MDRRMO Staff/Responders)
-- Includes roles, specialties (for targeted deployment), and contact info.
INSERT INTO Personnel (name, role, specialty, contact_number, assigned_unit) VALUES
('Ramos, Crispin S.', 'Commander', 'Logistics', '09171234567', 'Operations'),
('De Guzman, Maria A.', 'Logistics Officer', 'Procurement', '09199876543', 'Admin'),
('Cruz, John M.', 'Rescuer', 'Medical', '09202025128', 'Operations'),
('Santos, Anna R.', 'Rescuer', 'Search & Rescue', '09324443333', 'Operations');

-- 2. ResponseIncidents (Emergency Events)
-- Each incident is assigned a commander_id, demonstrating accountability.
INSERT INTO ResponseIncidents (incident_type, incident_location, date_reported, status, commander_id) VALUES
-- Incident 1: Commanded by Ramos (ID 1)
('Road Accident', 'Km 15, Maharlika Highway', '2025-12-06 08:00:00', 'Resolved', 1),
-- Incident 2: Commanded by Cruz (ID 3)
('Medical Emergency', 'Brgy. Sto. Angel Basketball Court', '2025-12-06 10:30:00', 'Active', 3),
-- Incident 3: Commanded by Ramos (ID 1)
('Flooding/Rescue', 'Sitio Lubog, Riverbank Area', '2025-12-06 14:00:00', 'Resolved', 1);

-- 3. Resources (Master Inventory List)
-- Includes vehicles, medical, and relief goods. Stock levels are simulated.
INSERT INTO Resources (item_name, category, stock_level, unit_of_measure) VALUES
('Ambulance 01', 'Vehicle', 1, 'Unit'),
('First Aid Kits', 'Medical Supplies', 30, 'Box'),
('Rope, 100m Rescue', 'Equipment', 5, 'Roll'),
('Bottled Water', 'Relief Goods', 500, 'Bottle');

-- 4. Deployment (Bridge Table: Personnel <-> Incidents)
-- Tracks which specific personnel were sent to which incident.
INSERT INTO Deployment (incident_id, personnel_id, deployment_time, role_during_incident) VALUES
-- Incident 1 Deployment:
(1, 1, '2025-12-06 08:05:00', 'Incident Command'), -- Ramos
(1, 3, '2025-12-06 08:06:00', 'Paramedic'), -- Cruz
-- Incident 2 Deployment:
(2, 3, '2025-12-06 10:35:00', 'On-Site Commander'), -- Cruz (as Commander)
(2, 4, '2025-12-06 10:35:00', 'Driver/Support'), -- Santos
-- Incident 3 Deployment:
(3, 1, '2025-12-06 14:05:00', 'Incident Command'), -- Ramos
(3, 4, '2025-12-06 14:06:00', 'Lead Rescuer'); -- Santos

-- 5. ResourceUsage (Bridge Table: Resources <-> Incidents)
-- Tracks the quantity of resources consumed during specific incidents for inventory deduction.
INSERT INTO ResourceUsage (incident_id, resource_id, quantity_used, date_used) VALUES
-- Usage for Incident 1 (Road Accident):
(1, 1, 1, '2025-12-06 08:10:00'), -- Used 1 Ambulance
(1, 2, 2, '2025-12-06 08:10:00'), -- Used 2 First Aid Kits
-- Usage for Incident 3 (Flooding/Rescue):
(3, 3, 1, '2025-12-06 14:15:00'), -- Used 1 Roll of Rope
(3, 4, 100, '2025-12-06 14:15:00'); -- Used 100 Bottles of Water