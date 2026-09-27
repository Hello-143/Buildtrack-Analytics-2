# Executive Recommendations: BuildTrack Analytics
**Gupta Engineers & Contractors — Noida Branch**

This report provides concrete, data-backed strategic recommendations to optimize cost margins, reduce timeline delays, and streamline vendor/labour management.

---

## 1. Vendor Strategy: Phase Out High-Wastage Local Vendors
The analysis of the material vendor records shows a stark difference between local Noida suppliers and corporate brand accounts in both delivery timeliness and material wastage.
- **Data Insight**: 
  - **Local Vendor Noida (Steel)** averages **13.21% wastage** and has a dismal **5.88% on-time delivery rate**.
  - **Local Vendor Cement** has **13.69% wastage** and a **0% on-time delivery rate** across 7 orders.
  - In comparison, national brands like **Tata Steel** maintain wastage at **7.91%** and achieve a **26.32% on-time delivery rate** (the highest in the dataset).
- **Recommendation**: Transition all steel and cement procurement away from local Noida suppliers to corporate supply accounts with Tata Steel and ACC. This change is projected to reduce average steel/cement wastage by over 5% and improve delivery reliability.

## 2. Project Budgeting: Establish 15% Contingency for Fabrication Contracts
Fabrication projects represent the highest risk area for financial overruns.
- **Data Insight**: Completed or delayed **Fabrication** projects experience an average **cost overrun of 12.84%**, compared to 8.90% for Residential and 2.36% for Building Contracts.
- **Recommendation**: Mandate a standard **15% contingency buffer** on all new Fabrication bids. Building Contracts require less buffer and can remain at 5%.

## 3. Labour Attendance: Set Warning Threshold at 80% Attendance
Labour availability is a core bottleneck.
- **Data Insight**: The Risk Model identified that **Average Labour Attendance %** is one of the top predictors of project risk, carrying a **40.54% importance weight** in predicting cost overrun risk.
- **Recommendation**: Implement an automated weekly flag in the reporting system. Any construction site (such as *Noida Sec 150 Site*) whose 14-day rolling attendance falls below **80%** must be flagged for manual intervention (e.g. subcontractor review, transport assistance) before the project falls into the "Delayed" status.

## 4. Prioritize Risk Monitoring on Short-to-Medium Duration Projects
Counterintuitively, planned project duration significantly impacts risk classification.
- **Data Insight**: The decision tree model identified **planned_duration** as the single highest driver of risk classification with a **42.81% feature importance**.
- **Recommendation**: Projects with planned durations under 90 days are most vulnerable to short-term disruptions. Establish a weekly standup cadence for all projects with planned durations under 90 days that have average wastage above 10% or average attendance below 85%.
