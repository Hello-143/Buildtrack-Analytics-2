# Dashboard Iteration & Change Log
**BuildTrack Analytics Dashboard — Noida Branch**

This log documents feedback from branch stakeholders and corresponding dashboard enhancements.

---

## [v1.2] - 2026-07-18
* **Feedback Source**: Managing Director, Noida Branch
* **Feedback / Request**: "The dashboards look good, but I can't quickly see which active projects are at risk of exceeding budget without clicking through every single card. I need a single view that displays predictive risk flags."
* **Action Taken**: 
  - Designed the **Executive Summary Page (Page 4)**.
  - Imported the Machine Learning risk predictions (`reports/risk_flags.csv`) into the dataset.
  - Added a **High Risk Project Alert List** on the main executive view using conditional formatting (Red highlight for High risk, Yellow for Medium).

---

## [v1.1] - 2026-07-10
* **Feedback Source**: Procurement Manager
* **Feedback / Request**: "The material dashboard doesn't highlight why local Noida suppliers are lagging. Can we visualize delivery rate side-by-side with wastage?"
* **Action Taken**:
  - Replaced the simple table with a **Vendor Performance Scatter Chart** comparing On-Time Delivery Rate % (X-axis) against Average Wastage % (Y-axis).
  - Divided the scatter plot into four quadrants: *Preferred Vendors* (bottom-right) vs. *High-Risk/Exit Vendors* (top-left).

---

## [v1.0] - 2026-07-02
* **Feedback Source**: Construction Site Supervisors (Noida Sector 62 & 150)
* **Feedback / Request**: "Initial layouts only showed raw present workers. It doesn't tell us if we are under-staffed. We need expected vs. present metrics."
* **Action Taken**:
  - Created a derived metric `attendance_pct` in the data cleaning pipeline.
  - Implemented the **Expected vs. Present Man-Days comparison** in the Labour page.
