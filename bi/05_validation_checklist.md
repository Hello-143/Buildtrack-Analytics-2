# BI QA & Validation Checklist
**BuildTrack Analytics Dashboard — Noida Branch**

This checklist must be executed before deploying dashboard updates to production.

---

## 1. Data Integrity and Row Counts

- [ ] **Row Count Match**: Check that total records loaded into Power BI match database metrics:
  - `projects`: 35 records
  - `material_vendor`: 205 records
  - `labour_attendance`: 2,728 records
- [ ] **Deduplication Check**: Assert that `projects[project_id]` contains 0 duplicate values.
- [ ] **Null/Blank Validation**: Assert that `budgeted_cost` contains 0 null values, and `actual_cost` has null values *only* for projects currently in "Ongoing" status (without final invoice).

---

## 2. Model & Relationship Integrity

- [ ] **Relationship Cardinality**: Assert that all relationships are `1-to-many` (from `projects` to fact tables) and the cross-filter direction is set to `Single` (filtering from `projects` to facts).
- [ ] **Orphaned Records**: Run a referential integrity check in SQL to verify zero material/attendance records exist without a matching `project_id`.
  ```sql
  SELECT COUNT(*) FROM material_vendor WHERE project_id NOT IN (SELECT project_id FROM projects);
  -- Expected output: 0
  ```

---

## 3. Measure Precision & Threshold Auditing

- [ ] **Cost Variance Test**: Select a completed project (e.g. *Gupta Fabrication Project 10*) and manually recalculate:
  $$\text{Cost Variance} = \frac{\text{Actual Cost} - \text{Budgeted Cost}}{\text{Budgeted Cost}}$$
  Verify the value matches Power BI's `Cost Variance %` measure.
- [ ] **Division Filter Test**: Slice by division (Residential, Fabrication, Building Contract) and ensure all KPI cards update correctly.
- [ ] **Wastage Rate Cap**: Check that no record has a negative wastage rate, and that median imputations for missing values did not introduce skewed statistical means.
