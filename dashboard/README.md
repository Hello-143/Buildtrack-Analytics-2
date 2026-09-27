# Interactive HTML Dashboard
**BuildTrack Analytics — Noida Branch**

This directory contains a web-based, client-rendered interactive dashboard designed to mirror the metrics, layout, and tabs specified in `powerbi/BuildTrack_Dashboard_notes.md`. 

It serves as a fully functional, code-based demo of the analytics solution.

---

## 1. Quick Start / How to Run

Because the dashboard reads from `dashboard/data.js` (which is pre-serialized directly from the SQLite database), **you can run the dashboard in two ways**:

### Option A: Double-Click (Direct local execution)
Simply double-click the `index.html` file in your file explorer. It will open and run in any modern web browser immediately. No servers are required.

### Option B: Local Web Server
To serve it over HTTP:
1. Open a terminal at the repository root folder (`buildtrack-analytics/`).
2. Start Python's built-in web server:
   ```bash
   python -m http.server 8000
   ```
3. Open your browser and navigate to:
   [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)

---

## 2. Data Flow Pipeline

The data rendered in the dashboard is 100% real and is generated through the cleaning/modeling pipeline. It updates dynamically using this pipeline:

```
[SQLite DB: buildtrack.db] + [Reports CSVs]
                    |
                    v (Execute Exporter)
      `python src/export_dashboard_data.py`
                    |
                    v (Writes output)
           [dashboard/data.js]
                    |
                    v (Imported by client-side scripts)
          [dashboard/index.html] (Interactive Charts via Chart.js)
```

To refresh the dashboard data after modifying database seeding or cleaning parameters:
1. Execute the python script:
   ```bash
   python src/export_dashboard_data.py
   ```
2. Refresh the browser tab running `index.html`.
