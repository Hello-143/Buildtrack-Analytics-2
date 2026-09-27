import pandas as pd
import numpy as np

def _parse_single_date(x):
    """
    Parses a single date value that may be in one of three known raw formats:
      - '%d/%m/%Y'  e.g. 18/02/2025   (always uses '/')
      - '%m-%d-%Y'  e.g. 02-18-2025   (uses '-', starts with 2-digit month)
      - '%Y-%m-%d'  e.g. 2025-02-18   (uses '-', starts with 4-digit year)

    NOTE: pandas' format='mixed' auto-detection is ambiguous for day/month
    values <= 12 (e.g. it silently swaps day/month), which previously caused
    planned_end_date to be parsed as an earlier date than start_date for some
    rows. We disambiguate explicitly using the separator and the length of
    the first token instead of relying on automatic guessing.
    """
    if pd.isna(x):
        return pd.NaT
    x = str(x).strip()
    if not x or x.lower() == "nat":
        return pd.NaT

    try:
        if "/" in x:
            return pd.to_datetime(x, format="%d/%m/%Y", errors="coerce")
        first_token = x.split("-")[0]
        if len(first_token) == 4:
            return pd.to_datetime(x, format="%Y-%m-%d", errors="coerce")
        else:
            return pd.to_datetime(x, format="%m-%d-%Y", errors="coerce")
    except (ValueError, TypeError):
        # Last-resort fallback for any unexpected format
        return pd.to_datetime(x, errors="coerce")


def clean_dates(df, date_cols):
    """
    Standardizes dates in the dataframe columns to YYYY-MM-DD string or datetime.
    Handles multiple raw date formats (see _parse_single_date) without the
    day/month ambiguity that pandas' format='mixed' introduces.
    """
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].apply(_parse_single_date)
    return df

def clean_projects(df_raw):
    """
    Cleans projects raw dataframe:
    - Standardizes date formats.
    - Title cases project_type and maps to correct options.
    - Deduplicates by project_id.
    - Validates status.
    - Handles missing actual_cost for Completed projects.
    """
    # Create copy
    df = df_raw.copy()
    
    # 1. Deduplicate by project_id (keep first)
    df = df.drop_duplicates(subset=["project_id"], keep="first")
    
    # 2. Clean dates
    df = clean_dates(df, ["start_date", "planned_end_date", "actual_end_date"])
    
    # 3. Clean project_type casing
    df["project_type"] = df["project_type"].astype(str).str.strip().str.title()
    # Map any odd strings if any
    type_map = {"Residential": "Residential", "Building Contract": "Building Contract", "Fabrication": "Fabrication"}
    df["project_type"] = df["project_type"].map(lambda x: type_map.get(x, "Other"))
    
    # 4. Clean status
    df["status"] = df["status"].astype(str).str.strip().str.title()
    
    # 5. Handle missing actual_cost for Completed projects:
    # If completed but actual_cost is null, fill with budgeted_cost
    mask_completed_null = (df["status"] == "Completed") & (df["actual_cost"].isna())
    df.loc[mask_completed_null, "actual_cost"] = df.loc[mask_completed_null, "budgeted_cost"]
    
    # Format dates as YYYY-MM-DD string for SQLite compatibility
    for col in ["start_date", "planned_end_date", "actual_end_date"]:
        df[col] = df[col].dt.strftime('%Y-%m-%d').where(df[col].notna(), None)
        
    return df

def clean_material_vendor(df_raw):
    """
    Cleans material_vendor raw dataframe:
    - Deduplicates by record_id.
    - Standardizes material_type (title case).
    - Cleans dates.
    - Imputes missing wastage_pct using median of that material_type.
    - Recalculates on_time column.
    """
    df = df_raw.copy()
    
    # 1. Deduplicate by record_id
    df = df.drop_duplicates(subset=["record_id"], keep="first")
    
    # 2. Clean material_type casing
    df["material_type"] = df["material_type"].astype(str).str.strip().str.title()
    
    # 3. Clean dates
    df = clean_dates(df, ["promised_delivery_date", "actual_delivery_date"])
    
    # 4. Impute missing wastage_pct using median for that material_type
    medians = df.groupby("material_type")["wastage_pct"].transform("median")
    df["wastage_pct"] = df["wastage_pct"].fillna(medians)
    # If any still null, fill with overall median
    df["wastage_pct"] = df["wastage_pct"].fillna(df["wastage_pct"].median())
    
    # 5. Recalculate on_time derived column
    # actual_delivery_date <= promised_delivery_date
    df["on_time"] = (df["actual_delivery_date"] <= df["promised_delivery_date"]).astype(int)
    
    # Format dates as YYYY-MM-DD string
    for col in ["promised_delivery_date", "actual_delivery_date"]:
        df[col] = df[col].dt.strftime('%Y-%m-%d').where(df[col].notna(), None)
        
    return df

def clean_labour_attendance(df_raw):
    """
    Cleans labour_attendance raw dataframe:
    - Deduplicates by record_id (or site_name, date, project_id combination).
    - Clean date format.
    - Derived column: attendance_pct = (workers_present / workers_expected) * 100.
    """
    df = df_raw.copy()
    
    # 1. Deduplicate by record_id
    df = df.drop_duplicates(subset=["record_id"], keep="first")
    
    # 2. Clean dates
    df = clean_dates(df, ["date"])
    
    # 3. Recalculate attendance_pct
    df["attendance_pct"] = (df["workers_present"] / df["workers_expected"]) * 100
    df["attendance_pct"] = df["attendance_pct"].round(2)
    
    # Format date as YYYY-MM-DD string
    df["date"] = df["date"].dt.strftime('%Y-%m-%d').where(df["date"].notna(), None)
    
    return df
