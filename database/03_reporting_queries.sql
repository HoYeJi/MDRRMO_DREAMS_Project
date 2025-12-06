-- 03_reporting_queries.sql: COMPLEX QUERIES (5 TABLES)
-- These reports utilize the M:M relationships (Deployment, ResourceUsage)

USE MDRRMO_DREAMS_DB;

-- 1. Incident Performance Report: Commander, Total Personnel Deployed, and Incident Type
-- Objective: Link incidents to their commander and count how many total personnel were deployed via the Deployment table.
SELECT
    I.incident_id,
    I.incident_type,
    P_Commander.name AS Incident_Commander,
    I.date_reported,
    COUNT(D.personnel_id) AS Total_Personnel_Deployed
FROM
    ResponseIncidents AS I
JOIN
    Personnel AS P_Commander ON I.commander_id = P_Commander.personnel_id
LEFT JOIN
    Deployment AS D ON I.incident_id = D.incident_id
GROUP BY
    I.incident_id, I.incident_type, P_Commander.name, I.date_reported
ORDER BY
    I.date_reported DESC;

-- 2. Personnel Utilization by Specialty: Which personnel were deployed, their role, and specialty
-- Objective: Show a detailed log of every responder's deployment and role for accountability and scheduling.
SELECT
    P.name,
    P.specialty,
    I.incident_type,
    D.deployment_time,
    D.role_during_incident
FROM
    Deployment AS D
JOIN
    Personnel AS P ON D.personnel_id = P.personnel_id
JOIN
    ResponseIncidents AS I ON D.incident_id = I.incident_id
ORDER BY
    D.deployment_time DESC;

-- 3. Detailed Resource Consumption per Incident
-- Objective: Find the exact items and quantities used for each incident, ensuring resource accountability.
SELECT
    I.incident_id,
    I.incident_location,
    R.item_name,
    RU.quantity_used,
    R.unit_of_measure
FROM
    ResourceUsage AS RU
JOIN
    ResponseIncidents AS I ON RU.incident_id = I.incident_id
JOIN
    Resources AS R ON RU.resource_id = R.resource_id
ORDER BY
    I.incident_id, R.item_name;

-- 4. Low-Stock Inventory Alert (Simple filter)
-- Objective: Identify items in the inventory that need immediate replenishment (e.g., stock level is 5 or below).
SELECT
    item_name,
    category,
    stock_level
FROM
    Resources
WHERE
    stock_level <= 5
ORDER BY
    stock_level ASC;

-- 5. Incidents Lacking Resources (Anti-Join Logic)
-- Objective: Identify incidents that were logged but had *no* associated resource usage logged (potential auditing gap).
SELECT
    I.incident_id,
    I.incident_type,
    I.date_reported
FROM
    ResponseIncidents AS I
LEFT JOIN
    ResourceUsage AS RU ON I.incident_id = RU.incident_id
WHERE
    RU.usage_id IS NULL;