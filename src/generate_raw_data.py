import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def main():
    print("Generating synthetic raw datasets...")
    
    # Create directories if they do not exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("notebooks", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("powerbi", exist_ok=True)
    
    random.seed(42)
    np.random.seed(42)

    # 1. Generate Projects
    num_projects = 35
    project_types = ["Residential", "Building Contract", "Fabrication"]
    
    projects_data = []
    
    # Date helper
    start_base = datetime(2025, 1, 1)
    
    for i in range(1, num_projects + 1):
        project_id = i
        project_type = random.choice(project_types)
        project_name = f"Gupta {project_type} Project {i}"
        
        # Start dates spread across early 2025
        start_date = start_base + timedelta(days=random.randint(0, 90))
        planned_duration = random.randint(60, 150) # in days
        planned_end_date = start_date + timedelta(days=planned_duration)
        
        # Determine status
        # Ongoing, Completed, Delayed
        # Introduce correlation factors
        # 1: High Wastage/Low attendance => Delayed & Overrun
        # We will determine the risk factor (0.0 to 1.0) for this project
        risk_factor = random.random()
        
        status_rand = random.random()
        if status_rand < 0.4:
            status = "Completed"
        elif status_rand < 0.75:
            status = "Ongoing"
        else:
            status = "Delayed"
            
        # If delayed or completed with overrun
        actual_end_date = None
        budgeted_cost = float(np.round(random.uniform(500000, 5000000), -3)) # INR e.g. 5 Lakh to 50 Lakh
        actual_cost = None
        
        if status == "Completed":
            # If high risk factor, higher cost overrun and longer delay
            if risk_factor > 0.6:
                overrun_pct = random.uniform(0.10, 0.35)
                delay_days = random.randint(15, 45)
            else:
                overrun_pct = random.uniform(-0.05, 0.08)
                delay_days = random.randint(-5, 10)
            
            actual_end_date = planned_end_date + timedelta(days=delay_days)
            actual_cost = budgeted_cost * (1 + overrun_pct)
        elif status == "Delayed":
            # Ongoing but delayed or completed but delayed
            # We treat delayed as ongoing but running late
            if risk_factor > 0.5:
                overrun_pct = random.uniform(0.12, 0.40)
            else:
                overrun_pct = random.uniform(0.02, 0.15)
            
            actual_cost = budgeted_cost * (1 + overrun_pct) # already exceeding budget
            # actual_end_date remains null since it's still running
        else: # Ongoing (on track)
            # Budgeted cost vs actual cost so far
            actual_cost = budgeted_cost * random.uniform(0.3, 0.8)
            actual_end_date = None
            
        projects_data.append({
            "project_id": project_id,
            "project_name": project_name,
            "project_type": project_type,
            "start_date": start_date,
            "planned_end_date": planned_end_date,
            "actual_end_date": actual_end_date,
            "budgeted_cost": budgeted_cost,
            "actual_cost": actual_cost,
            "status": status,
            "_risk_factor": risk_factor # Hidden column for data coherence
        })
        
    df_projects = pd.DataFrame(projects_data)
    
    # 2. Generate Material Vendor Records
    vendors = {
        "Steel": ["Tata Steel", "Jindal Steel", "Sail", "Local Vendor Noida"],
        "Cement": ["UltraTech", "Ambuja", "ACC", "Local Vendor Cement"],
        "Fabrication Sheet": ["Jindal Aluminium", "Hindalco", "Bhushan Steel", "Local Sheet Vendor"],
        "Other": ["Noida Hardware Mart", "Apex Traders", "Krishna Materials"]
    }
    
    material_records = []
    record_id = 1
    
    for idx, proj in df_projects.iterrows():
        p_id = proj["project_id"]
        rf = proj["_risk_factor"]
        
        # Number of material orders per project: 4 to 8
        num_orders = random.randint(4, 8)
        
        # Decide materials based on project type
        if proj["project_type"] == "Fabrication":
            mat_pool = ["Fabrication Sheet", "Steel", "Other"]
        elif proj["project_type"] == "Residential":
            mat_pool = ["Cement", "Steel", "Other"]
        else:
            mat_pool = ["Cement", "Steel", "Fabrication Sheet", "Other"]
            
        for _ in range(num_orders):
            m_type = random.choice(mat_pool)
            v_name = random.choice(vendors[m_type])
            
            ordered_qty = float(np.round(random.uniform(50, 500), 1))
            
            # Wastage and on-time depends on risk factor (rf) and vendor reliability
            # Noida local vendors have higher wastage and late deliveries on average
            is_local = "Local" in v_name or "Mart" in v_name or "Traders" in v_name or "Krishna" in v_name
            
            base_wastage = 0.08 if is_local else 0.03
            # If project is high risk (corresponds to bad management/poor storage), wastage is higher
            wastage_pct = (base_wastage + (rf * 0.07) + random.uniform(0.0, 0.04)) * 100
            
            # Delivery dates
            # Order happens during project duration
            days_offset = random.randint(5, int((proj["planned_end_date"] - proj["start_date"]).days) - 10)
            promised_date = proj["start_date"] + timedelta(days=days_offset)
            
            # Delivery delay
            base_delay = 5 if is_local else 1
            delay = int(base_delay + (rf * 8) + random.randint(-2, 3))
            if delay < -2: delay = -2
            
            actual_date = promised_date + timedelta(days=delay)
            
            # Delivered quantity might have shortfalls
            shortfall_pct = random.uniform(0, 0.05) if is_local else random.uniform(0, 0.01)
            delivered_qty = float(np.round(ordered_qty * (1 - shortfall_pct), 1))
            
            on_time = actual_date <= promised_date
            
            material_records.append({
                "record_id": record_id,
                "project_id": p_id,
                "material_type": m_type,
                "vendor_name": v_name,
                "ordered_qty": ordered_qty,
                "delivered_qty": delivered_qty,
                "wastage_pct": wastage_pct,
                "promised_delivery_date": promised_date,
                "actual_delivery_date": actual_date,
                "on_time": on_time
            })
            record_id += 1
            
    df_material = pd.DataFrame(material_records)

    # 3. Generate Labour Attendance Records
    labour_records = []
    lab_record_id = 1
    
    sites = ["Noida Sec 62 Site", "Noida Express Way Site", "Greater Noida Depot", "Noida Sec 150 Site"]
    
    for idx, proj in df_projects.iterrows():
        p_id = proj["project_id"]
        rf = proj["_risk_factor"]
        
        # Site assignment
        site_name = sites[p_id % len(sites)]
        
        # Generate daily attendance for 60 to 90 days from project start
        start_dt = proj["start_date"]
        # Determine actual period we have attendance data for
        days_to_generate = random.randint(60, 90)
        
        for d in range(days_to_generate):
            curr_date = start_dt + timedelta(days=d)
            
            # Workers expected: 20 to 50
            workers_expected = random.randint(20, 50)
            
            # Attendance rate depends negatively on risk factor
            # High risk projects have chronically lower attendance (e.g. 70-80% average)
            # Low risk projects have 90-95% attendance
            base_attendance_pct = 0.92 - (rf * 0.20) + random.uniform(-0.05, 0.05)
            base_attendance_pct = max(0.5, min(1.0, base_attendance_pct))
            
            workers_present = int(np.round(workers_expected * base_attendance_pct))
            workers_present = min(workers_present, workers_expected)
            
            attendance_pct = (workers_present / workers_expected) * 100
            
            labour_records.append({
                "record_id": lab_record_id,
                "project_id": p_id,
                "site_name": site_name,
                "date": curr_date,
                "workers_expected": workers_expected,
                "workers_present": workers_present,
                "attendance_pct": attendance_pct
            })
            lab_record_id += 1
            
    df_labour = pd.DataFrame(labour_records)

    # 4. Introduce Messiness & Save Raw Files
    print("Introducing realistic messiness (inconsistent casing, format discrepancies, duplicates, NaNs)...")
    
    # 4.1 Projects Messiness
    # - Inconsistent project_type casing: e.g. residential, RESIDENTIAL, Residential
    df_projects_messy = df_projects.copy()
    df_projects_messy["project_type"] = df_projects_messy["project_type"].apply(
        lambda x: x.lower() if random.random() < 0.2 else (x.upper() if random.random() < 0.1 else x)
    )
    # - Inconsistent dates format (some formatted as DD/MM/YYYY, some YYYY-MM-DD)
    def mess_date(dt):
        if pd.isna(dt): return dt
        r = random.random()
        if r < 0.15:
            return dt.strftime("%d/%m/%Y")
        elif r < 0.3:
            return dt.strftime("%m-%d-%Y")
        else:
            return dt.strftime("%Y-%m-%d")
            
    df_projects_messy["start_date"] = df_projects_messy["start_date"].apply(mess_date)
    df_projects_messy["planned_end_date"] = df_projects_messy["planned_end_date"].apply(mess_date)
    df_projects_messy["actual_end_date"] = df_projects_messy["actual_end_date"].apply(mess_date)
    
    # - Some actual cost missing (completed project with no final invoice processed yet)
    mask_completed = df_projects_messy["status"] == "Completed"
    missing_indices = df_projects_messy[mask_completed].sample(frac=0.1, random_state=42).index
    df_projects_messy.loc[missing_indices, "actual_cost"] = np.nan
    
    # - Duplicate rows (5% duplicates)
    dupes = df_projects_messy.sample(frac=0.05, random_state=42)
    df_projects_messy = pd.concat([df_projects_messy, dupes], ignore_index=True)
    
    # Drop the hidden risk factor from the final file
    df_projects_messy = df_projects_messy.drop(columns=["_risk_factor"], errors="ignore")
    
    # 4.2 Material Vendor Messiness
    df_material_messy = df_material.copy()
    # Inconsistent material_type casing
    df_material_messy["material_type"] = df_material_messy["material_type"].apply(
        lambda x: x.upper() if random.random() < 0.15 else x.lower() if random.random() < 0.1 else x
    )
    # Date formatting messiness
    df_material_messy["promised_delivery_date"] = df_material_messy["promised_delivery_date"].apply(mess_date)
    df_material_messy["actual_delivery_date"] = df_material_messy["actual_delivery_date"].apply(mess_date)
    # Introduce duplicate records
    dupes_mat = df_material_messy.sample(frac=0.04, random_state=42)
    df_material_messy = pd.concat([df_material_messy, dupes_mat], ignore_index=True)
    # Some null wastage values (e.g. 5% missing wastage)
    null_wastage_idx = df_material_messy.sample(frac=0.05, random_state=42).index
    df_material_messy.loc[null_wastage_idx, "wastage_pct"] = np.nan
    
    # 4.3 Labour Attendance Messiness
    df_labour_messy = df_labour.copy()
    # Date formatting messiness
    df_labour_messy["date"] = df_labour_messy["date"].apply(mess_date)
    # Set attendance_pct to nan so we have to derive it later (since it's a derived boolean/number)
    df_labour_messy["attendance_pct"] = np.nan
    # Introduce duplicate records
    dupes_lab = df_labour_messy.sample(frac=0.02, random_state=42)
    df_labour_messy = pd.concat([df_labour_messy, dupes_lab], ignore_index=True)

    # Save files
    # Projects as Excel
    df_projects_messy.to_excel("data/raw/projects_raw.xlsx", index=False)
    # Material vendor as CSV
    df_material_messy.to_csv("data/raw/material_vendor_raw.csv", index=False)
    # Labour attendance as CSV
    df_labour_messy.to_csv("data/raw/labour_attendance_raw.csv", index=False)
    
    print(f"Data generation complete. Files created:")
    print(f" - data/raw/projects_raw.xlsx ({len(df_projects_messy)} rows)")
    print(f" - data/raw/material_vendor_raw.csv ({len(df_material_messy)} rows)")
    print(f" - data/raw/labour_attendance_raw.csv ({len(df_labour_messy)} rows)")

if __name__ == "__main__":
    main()
