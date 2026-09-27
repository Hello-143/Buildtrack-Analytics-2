# Stakeholder Requirements Document
**BuildTrack Analytics Dashboard — Noida Branch**

## 1. Project Background & Audience
Gupta Engineers & Contractors (Noida Branch) operates multiple parallel engineering projects across three divisions: Residential Houses, Building Contracts, and Structural Fabrication. 

The target audience for this BI solution includes:
* **Managing Director / Branch Head**: Requires a summary of cost variances, overall delivery delays, and high-risk flags.
* **Project Directors / PMs**: Need project-level details on timeline deviations and labour availability.
* **Procurement & Vendor Managers**: Require performance scorecards to renegotiate vendor contracts.
* **HR & Site Supervisors**: Track daily labour attendance rates to address personnel shortfalls.

---

## 2. Business Objectives & Mapping to Dashboard Views
The dashboard must directly address the branch's core operational bottlenecks:

| Business Objective | Operational Issue | Dashboard Module / View |
|---|---|---|
| **Consolidate Scattered Data** | Projects are tracked in disjointed formats, making holistic tracking of budget and schedule overruns impossible. | **Project Overview View** & **Executive Summary** |
| **Control Material wastage** | Vendors deliver late and waste sheets, cement, and steel without oversight, eroding project profit margins. | **Material & Vendor Performance View** |
| **Mitigate Labour Shortages** | Low and volatile labour attendance causes delayed milestone completion. | **Labour & Attendance Analytics View** |
| **Proactive Risk Intervention** | Project managers react *after* overruns occur rather than flagging risk markers beforehand. | **Executive Summary (ML Risk Model integration)** |

---

## 3. Slicer and Filter Requirements
To facilitate granular exploration, stakeholders require interactive slicers across all dashboard views:
* **Division/Project Type**: Residential, Building Contract, Fabrication.
* **Project Status**: Ongoing, Completed, Delayed.
* **Timeline/Date Filters**: Dynamic sliders to filter by project start dates or daily attendance dates.
* **Vendor Slicers**: Multi-select dropdown for specific material suppliers.
* **Site Slicer**: Filter attendance metrics by physical work locations (e.g. Noida Sec 62, Sec 150).
