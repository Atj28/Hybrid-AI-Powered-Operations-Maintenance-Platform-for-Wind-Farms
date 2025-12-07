import pandas as pd
import numpy as np

from pathlib import Path
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
output_path = DATA_DIR / "turbine_health_scores.csv"


WINDOW_1D = 144            # 1 day
WINDOW_3D = 144 * 3        # 3 days
WINDOW_7D = 144 * 7        # 7 days

OIL_SLOPE_LIMIT = 8        # °C/day
VIB_SLOPE_LIMIT = 0.4      # g/day
YAW_LIMIT = 20             # degrees
OIL_ABSOLUTE_LIMIT = 85    # °C
VIB_ABSOLUTE_LIMIT = 1.5   # gRMS

def load_data():
    return pd.read_parquet(DATA_DIR/"wind_scada_clean.parquet")

def compute_trends(g):
    g = g.copy()
    g = g.sort_values("timestamp")

    # Rolling means
    g["oil_roll"] = g["gear_oil_temp_c"].rolling(WINDOW_1D).mean()
    g["vib_roll"] = g["vibration_g_rms"].rolling(WINDOW_1D).mean()

    # Slope/trend
    g["oil_slope"] = g["gear_oil_temp_c"].diff(WINDOW_1D)
    g["vib_slope"] = g["vibration_g_rms"].diff(WINDOW_1D)

    return g

def detect_warnings(g):
    g["oil_warning"] = (
        (g["gear_oil_temp_c"] > OIL_ABSOLUTE_LIMIT) |
        (g["oil_slope"] > OIL_SLOPE_LIMIT)
    )

    g["vib_warning"] = (
        (g["vibration_g_rms"] > VIB_ABSOLUTE_LIMIT) |
        (g["vib_slope"] > VIB_SLOPE_LIMIT)
    )

    g["yaw_warning"] = g["yaw_misalignment_deg"] > YAW_LIMIT

    return g

def compute_health_score(latest_row):
    score = 100

    if latest_row["gear_oil_temp_c"] > OIL_ABSOLUTE_LIMIT:
        score -= 30
    if latest_row["oil_slope"] > OIL_SLOPE_LIMIT:
        score -= 20

    if latest_row["vibration_g_rms"] > VIB_ABSOLUTE_LIMIT:
        score -= 30
    if latest_row["vib_slope"] > VIB_SLOPE_LIMIT:
        score -= 20

    if latest_row["yaw_misalignment_deg"] > YAW_LIMIT:
        score -= 10

    return max(score, 0)

def run_predictive_agent():
    df = load_data()
    results = []

    for tid, g in df.groupby("turbine_id"):
        g = compute_trends(g)
        g = detect_warnings(g)

        latest = g.iloc[-1]
        score = compute_health_score(latest)

        results.append({
            "turbine_id": tid,
            "health_score": score,
            "oil_temp": latest["gear_oil_temp_c"],
            "oil_slope": latest["oil_slope"],
            "vibration": latest["vibration_g_rms"],
            "vib_slope": latest["vib_slope"],
            "yaw": latest["yaw_misalignment_deg"]
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_path, index=False)
    print("Saved: data/turbine_health_scores.csv")

if __name__ == "__main__":
    run_predictive_agent()
