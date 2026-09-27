# KPI Catalog
**BuildTrack Analytics Dashboard — Noida Branch**

This catalog maps business metrics to physical data sources and thresholds.

---

## 1. Project Health KPIs

### KPI 1: Cost Variance %
* **Description**: The percentage deviation of actual costs from the planned budget.
* **Formula**: `(SUM(projects[actual_cost]) - SUM(projects[budgeted_cost])) / SUM(projects[budgeted_cost])`
* **Thresholds**: 
  * **Green (On track)**: $\le 2.0\%$
  * **Yellow (Warning)**: $2.1\% \text{ to } 10.0\%$
  * **Red (Critical Overrun)**: $> 10.0\%$
* **Source Table/Columns**: `projects[actual_cost]`, `projects[budgeted_cost]`

### KPI 2: Average Project Delay (Days)
* **Description**: Average deviation between the actual/reference completion date and planned end date.
* **Formula**: `AVERAGE(projects[delay_days])`
* **Thresholds**: 
  * **Green**: $\le 0 \text{ days}$
  * **Yellow**: $1 \text{ to } 15 \text{ days}$
  * **Red**: $> 15 \text{ days}$
* **Source Table/Columns**: `projects[delay_days]` (derived)

### KPI 3: Overrun Projects Count
* **Description**: Total count of active or completed projects that have breached their budgets.
* **Formula**: `CALCULATE(COUNT(projects[project_id]), projects[actual_cost] > projects[budgeted_cost])`
* **Source Table/Columns**: `projects[project_id]`, `projects[actual_cost]`, `projects[budgeted_cost]`

---

## 2. Material & Vendor Performance KPIs

### KPI 4: On-Time Delivery Rate %
* **Description**: Percentage of orders delivered on or before the promised delivery date.
* **Formula**: `DIVIDE(CALCULATE(COUNT(material_vendor[record_id]), material_vendor[on_time] = 1), COUNT(material_vendor[record_id])) * 100`
* **Thresholds**:
  * **Green**: $\ge 85.0\%$
  * **Yellow**: $70.0\% \text{ to } 84.9\%$
  * **Red (Critical Late Deliveries)**: $< 70.0\%$
* **Source Table/Columns**: `material_vendor[on_time]`

### KPI 5: Average Material Wastage %
* **Description**: The average wastage rate recorded during material handling at construction sites.
* **Formula**: `AVERAGE(material_vendor[wastage_pct])`
* **Thresholds**:
  * **Green**: $\le 5.0\%$
  * **Yellow**: $5.1\% \text{ to } 10.0\%$
  * **Red**: $> 10.0\%$
* **Source Table/Columns**: `material_vendor[wastage_pct]`

### KPI 6: Quantity Fulfillment Rate %
* **Description**: Proportion of ordered material quantity that was successfully delivered.
* **Formula**: `(SUM(material_vendor[delivered_qty]) / SUM(material_vendor[ordered_qty])) * 100`
* **Thresholds**:
  * **Green**: $\ge 99.0\%$
  * **Red**: $< 99.0\%$
* **Source Table/Columns**: `material_vendor[delivered_qty]`, `material_vendor[ordered_qty]`

---

## 3. Labour Attendance KPIs

### KPI 7: Average Labour Attendance %
* **Description**: The average presence of workers relative to expected headcount across sites.
* **Formula**: `AVERAGE(labour_attendance[attendance_pct])`
* **Thresholds**:
  * **Green**: $\ge 90.0\%$
  * **Yellow**: $80.0\% \text{ to } 89.9\%$
  * **Red (Severe Shortage)**: $< 80.0\%$
* **Source Table/Columns**: `labour_attendance[attendance_pct]`

### KPI 8: Expected vs. Actual Man-Days
* **Description**: Side-by-side comparison of planned vs. actual workforce volume in man-days.
* **Formula**:
  * *Expected*: `SUM(labour_attendance[workers_expected])`
  * *Actual*: `SUM(labour_attendance[workers_present])`
* **Source Table/Columns**: `labour_attendance[workers_expected]`, `labour_attendance[workers_present]`
