import sqlite3
import pandas as pd
import json
import os
from datetime import datetime, timezone

def main():
    print("Exporting data for the HTML dashboard...")
    
    # Paths
    db_path = "database/buildtrack.db"
    scorecard_path = "reports/vendor_scorecard.csv"
    risk_flags_path = "reports/risk_flags.csv"
    output_js_path = "dashboard/data.js"
    
    os.makedirs("dashboard", exist_ok=True)
    
    # 1. Read from SQLite
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run notebooks first.")
        return
        
    conn = sqlite3.connect(db_path)
    df_projects = pd.read_sql_query("SELECT * FROM projects", conn)
    df_mv = pd.read_sql_query("SELECT * FROM material_vendor", conn)
    df_lab = pd.read_sql_query("SELECT * FROM labour_attendance", conn)
    conn.close()
    
    # 2. Read from Reports
    df_scorecard = pd.read_csv(scorecard_path) if os.path.exists(scorecard_path) else pd.DataFrame()
    
    # Risk flags might have comment lines (#) at the top, let's read carefully
    risk_data = []
    if os.path.exists(risk_flags_path):
        with open(risk_flags_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("#"):
                    continue
                risk_data.append(line)
        # Parse from CSV lines
        from io import StringIO
        df_risk = pd.read_csv(StringIO("".join(risk_data)))
    else:
        df_risk = pd.DataFrame()
        
    # Convert dataframes to dictionaries/JSON
    projects_json = df_projects.to_dict(orient="records")
    material_vendor_json = df_mv.to_dict(orient="records")
    labour_attendance_json = df_lab.to_dict(orient="records")
    scorecard_json = df_scorecard.to_dict(orient="records")
    risk_flags_json = df_risk.to_dict(orient="records")

    # Export timestamp for dynamic System Status badge
    exported_at = datetime.now(timezone.utc).isoformat()
    
    # Write to data.js
    with open(output_js_path, "w", encoding="utf-8") as f:
        f.write("// BUILDTRACK ANALYTICS STATIC DATASET\n")
        f.write("// Generated automatically by src/export_dashboard_data.py\n\n")
        
        f.write(f"const exportedAt = {json.dumps(exported_at)};\n\n")
        f.write(f"const projectsData = {json.dumps(projects_json, indent=2)};\n\n")
        f.write(f"const materialVendorData = {json.dumps(material_vendor_json, indent=2)};\n\n")
        f.write(f"const labourAttendanceData = {json.dumps(labour_attendance_json, indent=2)};\n\n")
        f.write(f"const vendorScorecardData = {json.dumps(scorecard_json, indent=2)};\n\n")
        f.write(f"const riskFlagsData = {json.dumps(risk_flags_json, indent=2)};\n\n")
        
    print(f"Data exported successfully to {output_js_path}")
    print(f"exportedAt = {exported_at}")

if __name__ == "__main__":
    main()
