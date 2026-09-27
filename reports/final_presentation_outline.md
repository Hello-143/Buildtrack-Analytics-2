# Final Presentation Outline
**BuildTrack Analytics — Gupta Engineers Board Meeting**

This slide-by-slide structure outline is prepared for the executive presentation.

---

### Slide 1: Title Slide
* **Title**: Data-Driven Project Risk & Operations Review
* **Subtitle**: Noida Branch Performance Audit & BI Implementation
* **Presenter**: Lead Data Analyst + BI Engineer
* **Visual**: Clean minimalist title slide with branch branding.

### Slide 2: Context & Business Problem
* **Central Problem Statement**: Noida branch margin erosion from scattered data, unmonitored vendor wastage, and site labor absenteeism.
* **Scope**: 6-week audit of 35 projects, 205 procurement orders, and 2,728 labor records.
* **Goal**: Shift branch operations from reactive fire-fighting to proactive risk management.

### Slide 3: Unified Data Architecture
* **The Star Schema Solution**: Consolidated ERP Excel spreadsheets, vendor logs, and attendance databases into a unified SQLite database.
* **Key Components**:
  - `projects` (conformed dimension)
  - `material_vendor` (delivery performance fact table)
  - `labour_attendance` (daily attendance fact table)
* **Outcomes**: Removed data silos, reduced reporting latency from weekly to near-realtime.

### Slide 4: Project Cost & Timeline Variance Analysis
* **Key Visual**: Clustered column chart comparing Budgeted vs. Actual Cost.
* **Key Data Points**:
  - Across all completed or delayed projects, **Fabrication contracts** have the highest average overrun rate at **12.84%** (Average cost: INR 3.64M vs. Budget: INR 3.22M).
  - Residential projects average **8.90% cost overrun**.
  - Building Contracts are highly stable, averaging **2.36% cost overrun**.
* **Takeaway**: Bidding templates for Fabrication must include a 15% budget buffer.

### Slide 5: Vendor Scorecard: Identifying Procurement Leakage
* **Key Visual**: Performance Scatter Chart (Wastage Rate vs. On-Time Delivery Rate).
* **Key Data Points**:
  - **Local Noida suppliers** are primary drivers of waste. *Local Vendor Noida* averages **13.21% steel wastage** and only **5.88% on-time delivery**. *Local Vendor Cement* averages **13.69% wastage** and **0.0% on-time delivery**.
  - **Corporate Accounts** are highly efficient. *Tata Steel* averages **7.91% wastage** and **26.32% on-time delivery**. *ACC Cement* averages **8.00% wastage** and **10.0% on-time delivery**.
* **Strategic Move**: Phase out Noida local accounts. Transition to national account frameworks to save over INR 1.2M annually in wastage.

### Slide 6: Labour Absenteeism: The Hidden Project Delay Driver
* **Key Visual**: Expected vs. Present Man-Days comparison by site.
* **Key Data Points**:
  - Average labour attendance across all projects is **82.88%**.
  - Sites like *Noida Sector 150* experience chronic attendance dips down to **78%**.
  - Average project attendance has a strong positive correlation with final project delays: low-attendance sites experience an average timeline overrun of **14.2 days**.
* **Strategic Move**: Deploy automated site-level alerts when 14-day attendance falls below **80%**.

### Slide 7: Machine Learning Project Risk Model
* **Key Visual**: Feature Importance Bar Chart.
* **Model Highlights**:
  - **Planned Project Duration** (42.81% importance) and **Average Attendance** (40.54% importance) are the top predictive features of cost overruns.
  - The model identified **6 active projects** currently flagged as **High Risk** (e.g. *Gupta Fabrication Project 10*).
* **Strategic Move**: Standardize predictive risk mapping inside the Power BI Executive Summary view.

### Slide 8: Summary of Strategic Actions & Next Steps
* **Action 1**: Phase out high-waste local suppliers; prioritize national corporate accounts.
* **Action 2**: Mandate 15% contingency on Fabrication bids.
* **Action 3**: Integrate 80% attendance warning threshold alerts.
* **Action 4**: Roll out the 4-page Power BI Dashboard to Noida management by end-of-week.
