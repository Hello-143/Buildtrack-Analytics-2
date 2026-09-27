# Data Model Architecture
**BuildTrack Analytics Dashboard — Noida Branch**

This document describes the schema architecture designed for Power BI modeling.

---

## 1. Schema Layout: Star Schema

To optimize query speeds, filter propagation, and DAX calculations, the database schema is mapped as a **Star Schema** with `projects` acting as the central dimension (conformed dimension) and `material_vendor` and `labour_attendance` acting as transactional fact tables.

```
       +----------------------------+
       |   labour_attendance        | (Fact Table)
       +----------------------------+
       | record_id (PK)             |
       | project_id (FK)  <---------+
       | site_name                  |       |
       | date                       |       |
       | workers_expected           |       |
       | workers_present            |       |
       | attendance_pct             |       |
       +----------------------------+       |
                                            | (1-to-many relationship)
                                            |
       +----------------------------+       |
       |         projects           | (Dimension Table)
       +----------------------------+       |
       | project_id (PK)  ----------+-------+
       | project_name               |-------+
       | project_type               |       |
       | start_date                 |       |
       | planned_end_date           |       | (1-to-many relationship)
       | actual_end_date            |       |
       | budgeted_cost              |       v
       | actual_cost                |
       | status                     |
       +----------------------------+
                                            ^
       +----------------------------+       |
       |     material_vendor        | (Fact Table)
       +----------------------------+       |
       | record_id (PK)             |       |
       | project_id (FK)  ----------+-------+
       | material_type              |
       | vendor_name                |
       | ordered_qty                |
       | delivered_qty              |
       | wastage_pct                |
       | promised_delivery_date     |
       | actual_delivery_date       |
       | on_time                    |
       +----------------------------+
```

---

## 2. Table Specifications

### A. Dim_Projects (Dimension Table)
* **Description**: Conformed dimension containing master records for Noida branch projects.
* **Grain**: One row per project.
* **Fields**:
  * `project_id` (Primary Key, integer)
  * `project_name` (Text)
  * `project_type` (Text: Residential, Building Contract, Fabrication)
  * `start_date` (Date)
  * `planned_end_date` (Date)
  * `actual_end_date` (Date, Nullable)
  * `budgeted_cost` (Decimal, Currency)
  * `actual_cost` (Decimal, Currency, Nullable)
  * `status` (Text: Ongoing, Completed, Delayed)

### B. Fact_Material_Vendor (Fact Table)
* **Description**: Fact table capturing material deliveries, wastage, and delivery deviations.
* **Grain**: One row per purchase/delivery order.
* **Fields**:
  * `record_id` (Primary Key, integer)
  * `project_id` (Foreign Key linked to `projects[project_id]`, integer)
  * `material_type` (Text)
  * `vendor_name` (Text)
  * `ordered_qty` (Decimal)
  * `delivered_qty` (Decimal)
  * `wastage_pct` (Decimal)
  * `promised_delivery_date` (Date)
  * `actual_delivery_date` (Date)
  * `on_time` (Boolean / Whole Number: 1 = Yes, 0 = No)

### C. Fact_Labour_Attendance (Fact Table)
* **Description**: Fact table containing site-level worker attendance counts on a daily grain.
* **Grain**: One row per project, per site, per day.
* **Fields**:
  * `record_id` (Primary Key, integer)
  * `project_id` (Foreign Key linked to `projects[project_id]`, integer)
  * `site_name` (Text)
  * `date` (Date)
  * `workers_expected` (Whole Number)
  * `workers_present` (Whole Number)
  * `attendance_pct` (Decimal)
