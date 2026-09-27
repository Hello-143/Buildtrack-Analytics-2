# BuildTrack Analytics Dashboard
**Gupta Engineers & Contractors — Noida Branch**

A unified three-layer analytics solution designed to consolidate scattered project data, track vendor delivery reliability, audit material wastage, and analyze site-level labour attendance.

---

## 1. Project Architecture

```
                       [ RAW DATA INPUTS ]
             (projects_raw.xlsx, material_vendor_raw.csv, 
                  labour_attendance_raw.csv)
                            |
                            v
               [ PYTHON CLEANING PIPELINE ]
                 (src/cleaning.py, pandas)
                            |
             +--------------+--------------+
             |                             |
             v                             v
     [ PROCESSED CSVs ]           [ SQLITE DATABASE ]
     (data/processed/)        (database/buildtrack.db)
             |                             |
             |                   +---------+---------+
             |                   |                   |
             |                   v                   v
             |           [ SQL ANALYTICS ]    [ RISK MODEL ]
             |        (notebooks 02, 03, 04) (src/risk_model.py,
             |                   |            notebook 05)
             |                   |                   |
             v                   v                   v
      [ POWER BI SPEC ]   [ SCORES & PLOTS ]  [ RISK REPORT ]
     (powerbi/notes.md)     (reports/*.csv,     (risk_flags.csv)
                               reports/*.png)
```

---

## 2. Repository Structure

- `data/`
  - `raw/`: Raw Excel and CSV files containing messy synthetic data.
  - `processed/`: Standardized, deduped, and formatted CSV files.
- `database/`
  - `schema.sql`: MySQL database schema definition.
  - `buildtrack.db`: Populated SQLite database.
- `notebooks/`
  - `01_data_cleaning.ipynb`: Loads raw data, cleans it, and loads to database.
  - `02_project_analysis.ipynb`: Evaluates cost overruns and delays.
  - `03_material_vendor_analysis.ipynb`: Builds the Vendor Scorecard.
  - `04_labour_analysis.ipynb`: Evaluates labour trends and correlations.
  - `05_risk_model.ipynb`: Fits a Decision Tree Classifier for overrun risk.
- `src/`
  - `db_connection.py`: SQLite database connection helper.
  - `cleaning.py`: Reusable cleaning functions.
  - `risk_model.py`: Risk classification model helper.
  - `run_notebook.py`: Programmatic execution runner for notebook files.
- `reports/`
  - `vendor_scorecard.csv`: Vendor comparison scorecard.
  - `risk_flags.csv`: Project-level risk predictions and plain-English notes.
  - `final_recommendations.md`: Executive business recommendations.
- `powerbi/`
  - `BuildTrack_Dashboard_notes.md`: Detailed Power BI integration spec and DAX measures.

---

## 3. How to Run

### Step 1: Install Dependencies
Install all required libraries using pip:
```bash
pip install pandas openpyxl matplotlib seaborn scikit-learn
```

### Step 2: Generate Synthetic Raw Data
Run the generator to create the raw messy files:
```bash
python src/generate_raw_data.py
```

### Step 3: Run Jupyter Notebooks
Run the notebooks in sequence (either inside Jupyter or programmatically using the provided runner script):
```bash
python src/run_notebook.py notebooks/01_data_cleaning.ipynb
python src/run_notebook.py notebooks/02_project_analysis.ipynb
python src/run_notebook.py notebooks/03_material_vendor_analysis.ipynb
python src/run_notebook.py notebooks/04_labour_analysis.ipynb
python src/run_notebook.py notebooks/05_risk_model.ipynb
```

---

## 4. Key Findings

1. **Material Wastage**: Local Noida vendors have significantly higher wastage (~13.2% vs ~7.9% for corporate brands) and lower on-time delivery rates.
2. **Project Performance**: Fabrication projects are the most delay-prone and have the highest average cost overrun of **12.84%** when delayed/completed.
3. **Labour Risk**: Labour attendance carries a high predictor weight (**40.54%**) for overall project risk classification. Setting an 80% attendance alert threshold is key to mitigating delays.
