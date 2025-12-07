import pandas as pd
import numpy as np
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
path = DATA_DIR / "wind_scada_clean.parquet"

## load the cleaned SCADA DATA
def load_clean_scada():

    """
    Load the cleaned Scada data from the Parquet file.
    """
    print("path",path)
    df = pd.read_parquet(path)
    print("Loaded clean Scada shape", df.shape)
    return df


## Compute the Wind Farm-level KPIs
RATED_POWER_KW=2000
INTERVAL_MIN=10


def compute_farm_kpis(df):
    """
    Compute basic kpis for the whole wind farm.
    """

    # 1) Energy per row = power * hours
    hours_per_row = INTERVAL_MIN / 60.0
    df["energy_kwh"] = df["power_kw"] * hours_per_row

    # 2) Total energy
    total_energy_kwh =df["energy_kwh"].sum()
    print("Total energy", total_energy_kwh)

    # 3) Time span in hours
    time_span_hours = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 3600.0

    # 4) Installed capacity = number of turbines * rated power
    n_turbines = df["turbine_id"].nunique()
    installed_kw = n_turbines * RATED_POWER_KW

    # 5) Capacity factor = actual energy /(installed*time)
    capacity_factor = total_energy_kwh / (installed_kw * time_span_hours)

    # 6) Availability = fraction of time NOT in fault (status_code == 2)
    fault_fraction = (df["status_code"] == 2).mean()
    availability = 1.0 - fault_fraction

    # Put into dictionary 
    kpis = {
        "n_turbines": int(n_turbines),
        "total_energy_kwh": float(total_energy_kwh),
        "capacity_factor": float(capacity_factor),
        "availability": float(availability)
    }
    print(kpis)
    return kpis

## idividual performance
def compute_per_turbine_kpis(df):
    """
    Compute KPIs per turbine (energy, CF, availability).
    """
    hours_per_row = INTERVAL_MIN / 60.0
    df["energy_kwh"] = df["power_kw"] * hours_per_row

    # Total number of hours in the dataset
    time_span_hours = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 3600.0

    # Group by turbine_id
    grouped = (
        df.groupby("turbine_id")
          .agg(
              energy_kwh=("energy_kwh", "sum"),
              fault_fraction=("status_code", lambda s: (s == 2).mean())
          )
          .reset_index()
    )

    # Capacity factor per turbine
    grouped["capacity_factor"] = grouped["energy_kwh"] / (RATED_POWER_KW * time_span_hours)

    # Availability per turbine
    grouped["availability"] = 1.0 - grouped["fault_fraction"]
    print(grouped)
    return grouped

def build_power_curve(df, bin_width=0.5):
    """
    Build an empirical power curve:
    - Bin wind_speed into range of 'bin_width'
    - Compute average power in each bin
    """
    df =df.copy()
    # np.arange(start, stop, step) → create numbers from 0 → max in steps of 0.5
    bins = np.arange(0,df["wind_speed"].max() + bin_width, bin_width)

    df["wind_bin"] = pd.cut(df["wind_speed"], bins, right=False)

    pc = (
    df.groupby("wind_bin")["power_kw"]
      .agg(["mean", "count"])
      .reset_index()
      .rename(columns={"mean": "mean_power_kw"})
    )
    pc["ws_center"] = pc["wind_bin"].apply(lambda x: x.left + bin_width / 2)

    """
    Each bin is something like:
    #[5.0–5.5)
    #x.left = 5.0
    #bin_width / 2 = 0.25
    #Center = 5.0 + 0.25 = 5.25
    #This is useful for plotting the power curve.
    """
    print(pc)
    return pc


def detect_underperformance(df, pc, threshold_pct=0.2):
    """
    Flag rows where actual power is more than 'threshold_pct' below expected.

    threshold_pct = 0.2  → 20% below expected.
    """
    df = df.copy()

    # Make a mapping: ws_center → mean_power_kw
    pc_map = dict(zip(pc["ws_center"].round(2), pc["mean_power_kw"]))
    centers = sorted(pc_map.keys())

    # Helper function to get expected power for a given wind speed
    def expected_power(ws):
        if np.isnan(ws):
            return np.nan
        # Find nearest wind-speed bin center
        nearest_idx = min(range(len(centers)), key=lambda i: abs(centers[i] - round(ws, 2)))
        return pc_map[centers[nearest_idx]]

    # Apply to each row
    df["expected_power_kw"] = df["wind_speed"].apply(expected_power)

    # Relative difference: (expected - actual) / expected
    df["rel_diff"] = (df["expected_power_kw"] - df["power_kw"]) / (df["expected_power_kw"] + 1e-6)

    # Underperformance flag: more than threshold_pct below expected
    df["underperf_flag"] = df["rel_diff"] > threshold_pct

    return df

def main():
    # 1) Load cleaned data
    df = load_clean_scada()

    # 2) Farm KPIs
    farm_kpis = compute_farm_kpis(df)
    print("=== FARM KPIs ===")
    for k, v in farm_kpis.items():
        print(f"{k}: {v}")
    print()

    # 3) Per-turbine KPIs
    per_turbine = compute_per_turbine_kpis(df)
    print("=== PER-TURBINE KPIs ===")
    print(per_turbine)
    print()

    # 4) Build power curve and save
    pc = build_power_curve(df)
    power_curve_path = DATA_DIR / "power_curve_empirical.csv"
    pc.to_csv(power_curve_path, index=False)
    print(f"Saved power curve to: {power_curve_path}")

    # 5) Detect underperformance and save
    df_with_flags = detect_underperformance(df, pc, threshold_pct=0.2)
    print(f"Columns in df_with_flags: {df_with_flags.columns.tolist()}")
    print(f"Sample of df_with_flags:\n{df_with_flags[['wind_speed', 'power_kw', 'expected_power_kw', 'rel_diff', 'underperf_flag']].head()}")
    underperf = df_with_flags[df_with_flags["underperf_flag"]]

    underperf_cols = [
        "timestamp",
        "turbine_id",
        "wind_speed",
        "power_kw",
        "expected_power_kw",
        "rel_diff",
        "status_code",
        "alarm_code",
        "underperf_flag",
    ]
    underperf_path = DATA_DIR / "underperformance_events.csv"
    
    # Only select columns that exist in the dataframe
    available_cols = [col for col in underperf_cols if col in underperf.columns]
    print(f"Saving columns: {available_cols}")
    underperf[available_cols].to_csv(underperf_path, index=False)

    print(f"Saved underperformance events to: {underperf_path}")
    print(f"Total underperformance rows: {len(underperf)}")

if __name__ == "__main__":
    main()
