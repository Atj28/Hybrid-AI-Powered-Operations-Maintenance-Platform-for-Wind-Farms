import pandas as pd
from pathlib import Path

DATA_DIR=Path(__file__).resolve().parents[1] / "data"

def read_scada_csv(filename: str) -> pd.DataFrame:
    """
    MCP-style tool:read scada CSV from the data directory.
    """

    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path, parse_dates=['timestamp'])
    print(df.head(10))
    df = df.sort_values(['turbine_id', 'timestamp']).reset_index(drop=True)
    print(df.head(10))
    return df


if __name__ == "__main__":
    read_scada_csv("wind_scada_5turbines_1month_realistic.csv")