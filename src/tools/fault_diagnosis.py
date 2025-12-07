import pandas as pd
import numpy as np
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
scada_path = DATA_DIR / "wind_scada_clean.parquet"
underperf_path = DATA_DIR / "underperformance_events.csv"
output_path = DATA_DIR / "fault_diagnosis_results.csv"

## load the cleaned SCADA DATA
def load_clean_scada():
    """
    Load the cleaned Scada data from the Parquet file.
    """
    print("path",scada_path)
    scada_df = pd.read_parquet(scada_path)
    print("Loaded clean Scada shape", scada_df.shape)
    underperf = pd.read_csv(underperf_path, parse_dates=['timestamp'])
    print("Loaded underperformance events shape", underperf.shape)
    return scada_df, underperf

## DEFINE THRESHOLDS

# Gearbox and nacelle thresholds
GEAR_OIL_TEMP_LIMIT = 85 # °C
NACELLE_TEMP_LIMIT = 70 # °C

# Vibration threshold (RMS)
VIB_HIGH_LIMIT = 1.5 # g-RMS

# Yaw misalignment threshold
YAW_LIMIT = 15 # degrees
# Pitch stuck threshold

PITCH_STUCK_ANGLE = 0.5 # pitch near zero for long time

# Gearbox overtemperature detection
def detect_gearbox_fault(row):
    if row["gear_oil_temp_c"] > GEAR_OIL_TEMP_LIMIT:
        return "GEARBOX_OVERHEAT"
    return None

# High vibration fault
def detect_vibration_fault(row):
    if row["vibration_g_rms"] > VIB_HIGH_LIMIT:
        return "HIGH_VIBRATION"
    return None

# Pitch stuck fault
def detect_pitch_stuck(row):
    """
    Condition:
        -pitch angle stays near 0
        -underperformance flag
        -or alarm present
    """
    if row["pitch_angle_deg"] < PITCH_STUCK_ANGLE and row["power_kw"] < row["expected_power_kw"] * 0.3:
        return "PITCH_STUCK"
    return None

# Yaw misalignment
def detect_yaw_misalignment(row):
    """
    Large misalignment → low power for given wind
    """
    if abs(row["yaw_misalignment_deg"]) > YAW_LIMIT and row["underperf_flag"]:
        return "YAW_MISALIGNMENT"
    return None

# Grid-related curtailment(low fault severity)
def detect_grid_event(row):
    if row["grid_event"] != "NA":
        return "GRID_EVENT"
    return None

# Combining all diagnosis function
def diagnose_row(row):
    faults = []

    f1 = detect_gearbox_fault(row)
    if f1: faults.append(f1)

    f2 = detect_vibration_fault(row)
    if f2: faults.append(f2)

    f3 = detect_pitch_stuck(row)
    if f3: faults.append(f3)

    f4 = detect_yaw_misalignment(row)
    if f4: faults.append(f4)

    f5 = detect_grid_event(row)
    if f5: faults.append(f5)

    return ", ".join(faults) if faults else "NO_FAULT"

def run_diagnosis(scada, underperf):
    """
    Merge underperformance data with SCADA full dataset.
    Then apply rule-based diagnosis row by row.
    """
    # Merge expected_power and underperformance flag back into SCADA
    merged = scada.merge(
        underperf[["timestamp", "turbine_id", "expected_power_kw", "underperf_flag"]],
        on=["timestamp", "turbine_id"],
        how="left"
    )

    merged["expected_power_kw"] = merged["expected_power_kw"].fillna(merged["power_kw"])
    merged["underperf_flag"] = merged["underperf_flag"].fillna(False)

    print("Merged dataset shape:", merged.shape)

    # Apply diagnosis
    merged["diagnosis"] = merged.apply(diagnose_row, axis=1)

    return merged


def save_output(df):
    out_file = output_path
    df.to_csv(out_file, index=False)
    print(f"Saved diagnosis file: {out_file}")

def main():
    scada, underperf = load_clean_scada()
    diagnosed = run_diagnosis(scada, underperf)
    save_output(diagnosed)

if __name__ == "__main__":
    main()