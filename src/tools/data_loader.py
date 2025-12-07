import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def load_and_clean_data(
    input_filename: str = "wind_scada_5turbines_1month_realistic.csv",
    output_filename: str = "wind_scada_clean.parquet"
    ):
    """
    Load and clean data from a CSV file.
    """
    input_path = DATA_DIR / input_filename
    df = pd.read_csv(input_path, parse_dates=['timestamp'])
    print("Loaded shape: ", df.shape)
    print("Columns: ", df.columns)
    print("Data types: ", df.dtypes)


    # Identify string and numeric columns
    string_cols = df.select_dtypes(include=["object","string"]).columns.tolist()
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    print("String columns: ", string_cols)
    print("Numeric columns: ", numeric_cols)

    # check the missing value in string columns
    print(df[string_cols].isna().sum())

    #fill misiing in string columns
    df[string_cols] = df[string_cols].fillna('NA')

    #check missing value after filling 'NA'
    print(df[string_cols].isna().sum())

    # check missing numeric values
    print(df[numeric_cols].isna().sum())

    #sort by turbine_id and timestamp
    df =df.sort_values(['turbine_id', 'timestamp']).reset_index(drop=True)
    ## if any missing numeric columns we can use interpolation
    df[numeric_cols] = df[numeric_cols].interpolate(
        method="linear", limit=3, limit_direction="both")

    # numeric column after interpolation
    print(df[numeric_cols].isna().sum())

    ## Save Cleaned data
    output_path = DATA_DIR / output_filename
    df.to_parquet(output_path, index=False)


if __name__ == "__main__":
    load_and_clean_data()