# Executive Summary: BuildTrack Dashboard
**Gupta Engineers & Contractors — Noida Branch**

This summary condenses the operational and financial performance metrics derived from the BuildTrack Analytics project.

---

## 1. Project Health & Financial Summary

| Metrics | Total Value (Noida Branch) | Key Insight |
|---|---|---|
| **Total Projects Reviewed** | 35 Projects | Spread across Residential, Fabrication, and Building Contract types. |
| **Total Budgeted Cost** | INR 94.27M | Sum of initial planned project budgets. |
| **Total Cost Incurred (Actual/Ongoing)** | INR 84.14M | Total spend recorded up to July 18, 2026. |
| **Average Project Delay** | 14.2 Days | Fabrication projects face the highest delays (average 19.5 days). |

### Overrun Breakdown by Division (Completed/Delayed Projects)
- **Fabrication**: Average **12.84% cost overrun** (Actual: INR 3.64M vs. Budget: INR 3.22M).
- **Residential**: Average **8.90% cost overrun** (Actual: INR 2.29M vs. Budget: INR 2.05M).
- **Building Contract**: Average **2.36% cost overrun** (Actual: INR 2.68M vs. Budget: INR 2.56M).

---

## 2. Procurement & Vendor Analysis
An evaluation of 205 vendor delivery records shows that **material wastage** and **unreliable delivery dates** are primary drivers of margin erosion.

- **Wastage Statistics**: Average material wastage stands at **10.42%**.
  - *Cement* has the highest wastage rate at **10.74%**.
  - *Steel* has a wastage rate of **9.67%**.
- **Vendor Reliability Scorecard**:
  - **Tata Steel** is the most reliable supplier with an **on-time delivery rate of 26.32%** and a low wastage rate of **7.91%**.
  - **Local Vendor Noida (Steel)** is highly inefficient, with **13.21% average wastage** and only **5.88% on-time delivery**.
  - **Local Vendor Cement** has a **0% on-time delivery rate** and an average **13.69% wastage rate**.

---

## 3. Labour Attendance Audit
Labour presence heavily impacts project completion timelines.
- **Attendance Rate**: The branch averages **82.88% daily attendance**.
- **Low-Performing Sites**: The *Noida Sector 150* site records the lowest attendance, averaging **78%**.
- **Impact**: Correlation analysis shows that projects with average attendance below 80% experience an average schedule delay of **14.2 days**, confirming labour attendance as a key predictor of timeline health.

---

## 4. ML Risk Model Predictions
A Decision Tree Classifier trained on completed projects categorized active branch projects:
- **Risk Distribution**:
  - **6 Projects** classified as **High Risk** of cost overrun.
  - **14 Projects** classified as **Medium Risk**.
  - **15 Projects** classified as **Low Risk**.
- **Key Risk Drivers**:
  1. *Planned Duration* (42.81% relative importance weight)
  2. *Average Attendance %* (40.54% relative importance weight)
  3. *Average Wastage %* (16.65% relative importance weight)
