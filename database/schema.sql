-- Schema definitions for BuildTrack Analytics Dashboard
-- Gupta Engineers & Contractors — Noida Branch

-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS buildtrack_db;
USE buildtrack_db;

-- 1. Projects Table
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    project_type VARCHAR(50) NOT NULL, -- 'Residential', 'Building Contract', 'Fabrication'
    start_date DATE NOT NULL,
    planned_end_date DATE NOT NULL,
    actual_end_date DATE DEFAULT NULL,
    budgeted_cost DECIMAL(12, 2) NOT NULL,
    actual_cost DECIMAL(12, 2) DEFAULT NULL,
    status VARCHAR(20) NOT NULL -- 'Ongoing', 'Completed', 'Delayed'
);

-- 2. Material & Vendor Table
CREATE TABLE IF NOT EXISTS material_vendor (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    material_type VARCHAR(50) NOT NULL, -- 'Steel', 'Cement', 'Fabrication Sheet', 'Other'
    vendor_name VARCHAR(100) NOT NULL,
    ordered_qty DECIMAL(10, 2) NOT NULL,
    delivered_qty DECIMAL(10, 2) NOT NULL,
    wastage_pct DECIMAL(5, 2) NOT NULL, -- percentage e.g. 5.25 for 5.25%
    promised_delivery_date DATE NOT NULL,
    actual_delivery_date DATE NOT NULL,
    on_time BOOLEAN NOT NULL, -- derived: actual_delivery_date <= promised_delivery_date
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

-- 3. Labour Attendance Table
CREATE TABLE IF NOT EXISTS labour_attendance (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    site_name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    workers_expected INT NOT NULL,
    workers_present INT NOT NULL,
    attendance_pct DECIMAL(5, 2) NOT NULL, -- derived: (workers_present / workers_expected) * 100
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);
