import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sqlite3

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False


def prepare_features(conn):
    """
    Queries projects, material_vendor, and labour_attendance to build a features dataframe.
    Includes:
      - planned_duration
      - avg_wastage_pct
      - avg_attendance_pct
      - attendance_trend_4wk  (rolling 4-week trend of attendance)
      - vendor_delay_std      (std of delivery delay days across vendors for the project)
    """
    # 1. Projects basic info
    df_proj = pd.read_sql_query("SELECT * FROM projects", conn)
    df_proj["start_date"] = pd.to_datetime(df_proj["start_date"])
    df_proj["planned_end_date"] = pd.to_datetime(df_proj["planned_end_date"])
    df_proj["actual_end_date"] = pd.to_datetime(df_proj["actual_end_date"])

    df_proj["planned_duration"] = (df_proj["planned_end_date"] - df_proj["start_date"]).dt.days
    df_proj["cost_overrun_pct"] = (
        (df_proj["actual_cost"] - df_proj["budgeted_cost"]) / df_proj["budgeted_cost"]
    ) * 100

    # 2. Avg material wastage per project
    df_mv = pd.read_sql_query("SELECT * FROM material_vendor", conn)
    df_wastage = (
        df_mv.groupby("project_id")["wastage_pct"]
        .mean()
        .reset_index(name="avg_wastage_pct")
    )

    # 3. Vendor delay variability (std of delay days) per project
    df_mv["promised_delivery_date"] = pd.to_datetime(df_mv["promised_delivery_date"])
    df_mv["actual_delivery_date"] = pd.to_datetime(df_mv["actual_delivery_date"])
    df_mv["delay_days"] = (
        df_mv["actual_delivery_date"] - df_mv["promised_delivery_date"]
    ).dt.days
    df_delay_std = (
        df_mv.groupby("project_id")["delay_days"]
        .std()
        .reset_index(name="vendor_delay_std")
    )
    df_delay_std["vendor_delay_std"] = df_delay_std["vendor_delay_std"].fillna(0)

    # 4. Avg labour attendance + 4-week rolling trend per project
    df_lab = pd.read_sql_query("SELECT * FROM labour_attendance", conn)
    df_lab["date"] = pd.to_datetime(df_lab["date"])

    df_attendance = (
        df_lab.groupby("project_id")["attendance_pct"]
        .mean()
        .reset_index(name="avg_attendance_pct")
    )

    # Rolling 4-week trend: slope of weekly avg attendance over last 4 weeks
    def _attendance_trend(group):
        weekly = (
            group.set_index("date")["attendance_pct"]
            .resample("W")
            .mean()
            .dropna()
        )
        if len(weekly) < 2:
            return 0.0
        recent = weekly.tail(4)
        if len(recent) < 2:
            return 0.0
        # Simple linear slope (change per week)
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent.values, 1)[0]
        return float(slope)

    trends = (
        df_lab.groupby("project_id")
        .apply(_attendance_trend, include_groups=False)
        .reset_index(name="attendance_trend_4wk")
    )

    # Merge all
    df_features = df_proj.merge(df_wastage, on="project_id", how="left")
    df_features = df_features.merge(df_attendance, on="project_id", how="left")
    df_features = df_features.merge(df_delay_std, on="project_id", how="left")
    df_features = df_features.merge(trends, on="project_id", how="left")

    # Fill nulls
    for col in ["avg_wastage_pct", "avg_attendance_pct", "vendor_delay_std", "attendance_trend_4wk"]:
        if col in df_features.columns:
            med = df_features[col].median()
            df_features[col] = df_features[col].fillna(med if pd.notna(med) else 0)

    return df_features


def define_risk_label(overrun_pct):
    """Categorize risk based on cost overrun percentage."""
    if pd.isna(overrun_pct):
        return None
    if overrun_pct > 10.0:
        return "High"
    elif overrun_pct > 0.0:
        return "Medium"
    else:
        return "Low"


def train_and_predict(df_features):
    """
    Trains a DecisionTreeClassifier on completed projects and predicts risk for all.
    Returns: df_results, model, importances, encoded_feature_cols, X_all
    """
    df_features = df_features.copy()
    df_features["true_risk_label"] = df_features["cost_overrun_pct"].apply(define_risk_label)

    df_train = df_features[df_features["status"] == "Completed"].copy()
    if len(df_train) < 5:
        df_train = df_features.copy()
        df_train["true_risk_label"] = df_train["true_risk_label"].fillna("Medium")

    feature_cols = [
        "planned_duration",
        "avg_wastage_pct",
        "avg_attendance_pct",
        "attendance_trend_4wk",
        "vendor_delay_std",
    ]

    df_encoded = pd.get_dummies(df_features, columns=["project_type"], prefix="type")
    encoded_feature_cols = feature_cols + [
        c for c in df_encoded.columns if c.startswith("type_")
    ]

    X_train = df_encoded.loc[df_train.index, encoded_feature_cols]
    y_train = df_train["true_risk_label"]

    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    X_all = df_encoded[encoded_feature_cols]
    df_features["predicted_risk_label"] = model.predict(X_all)

    importances = dict(zip(encoded_feature_cols, model.feature_importances_))

    return df_features, model, importances, encoded_feature_cols, X_all


def get_top_shap_reasons(model, X_all, encoded_feature_cols, df_results, top_n=2):
    """
    Compute per-project SHAP values and return top-N feature reasons.
    Requires `shap` package. Falls back to feature-importance ranking if unavailable.
    """
    feature_name_map = {
        "planned_duration": "Planned project duration",
        "avg_wastage_pct": "Average material wastage %",
        "avg_attendance_pct": "Average labour attendance %",
        "attendance_trend_4wk": "4-week attendance trend",
        "vendor_delay_std": "Vendor delivery delay variability",
    }

    rows = []

    if HAS_SHAP:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_all)
        classes = list(model.classes_)

        for i, (idx, row) in enumerate(df_results.iterrows()):
            pred_label = row["predicted_risk_label"]
            class_idx = classes.index(pred_label) if pred_label in classes else 0

            # Handle different shap return shapes across versions:
            # - list of arrays: one per class, each (n_samples, n_features)
            # - 2D array: (n_samples, n_features) for binary
            # - 3D array: (n_samples, n_features, n_classes)
            if isinstance(shap_values, list):
                sv = shap_values[class_idx][i]
            elif getattr(shap_values, "ndim", 0) == 3:
                sv = shap_values[i, :, class_idx]
            else:
                sv = shap_values[i]

            pairs = sorted(
                zip(encoded_feature_cols, sv),
                key=lambda x: abs(x[1]),
                reverse=True,
            )[:top_n]

            reasons = {}
            for j, (feat, val) in enumerate(pairs, 1):
                nice = feature_name_map.get(feat, feat)
                direction = "increased" if val > 0 else "decreased"
                reasons[f"top_reason_{j}"] = f"{nice} {direction} risk (SHAP {val:+.2f})"

            rows.append({"project_id": row["project_id"], **reasons})
    else:
        # Fallback: use global feature importance order
        sorted_feats = sorted(
            zip(encoded_feature_cols, model.feature_importances_),
            key=lambda x: x[1],
            reverse=True,
        )
        for _, row in df_results.iterrows():
            reasons = {}
            for j in range(1, top_n + 1):
                if j - 1 < len(sorted_feats):
                    feat, imp = sorted_feats[j - 1]
                    nice = feature_name_map.get(feat, feat)
                    reasons[f"top_reason_{j}"] = f"{nice} (importance {imp:.2f})"
                else:
                    reasons[f"top_reason_{j}"] = "—"
            rows.append({"project_id": row["project_id"], **reasons})

    return pd.DataFrame(rows)
