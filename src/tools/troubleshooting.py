import pandas as pd
from .troubleshooting_knowledge import TROUBLESHOOTING_KB

from pathlib import Path
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
output_path = DATA_DIR / "troubleshooting_recommendations.csv"

def load_diagnosis():
    """
    Load the fault diagnosis results from the CSV file.
    """
    path = DATA_DIR / "fault_diagnosis_results.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"])
    print("Loaded fault diagnosis shape", df.shape)
    return df

def get_knowledge_for_fault(fault_label:str):
    """
    Map a diagnosis string to a knowledge base entry.
    If multiple faults exist in a row, use the first known one.
    """
    if not isinstance(fault_label,str):
        return TROUBLESHOOTING_KB["NO_FAULT"]
    
    # many rows may have Fault1,Fault2 etc split by comma
    parts = [p.strip()for p in fault_label.split(",")]


    for part in parts:
        if part in TROUBLESHOOTING_KB:
            return TROUBLESHOOTING_KB[part]
    
    # if nothing mathces
    return TROUBLESHOOTING_KB["NO_FAULT"]

def attach_troubleshooting(df):
    """
    For each row, attach description, severity, and recommended actions
    based on the diagnosis column.
    """
    description =[]
    severities =[]
    actions = []

    #df.iterrows() → goes through each row in the DataFrame
    #row → gives you the contents of that row as a Series (like a small dictionary)
    #_ → this means “ignore the index”, we don't need row index
    for _,row in df.iterrows():
        kb = get_knowledge_for_fault(row["diagnosis"])
        description.append(kb["description"])
        severities.append(kb["severity"])
        # join list of actions into one string
        actions.append(" | ".join(kb["recommended_actions"]))

    df["fault_description"] = description
    df["fault_severity"] = severities
    df["recommended_actions"] = actions

    return df
    
def main():
    df = load_diagnosis()
    df_with_troubleshooting = attach_troubleshooting(df)

    out_file = output_path
    df_with_troubleshooting.to_csv(out_file, index=False)
    print(f"Saved troubleshooting file: {out_file}")
    print("Sample rows:")
    print(df_with_troubleshooting[[
        "timestamp", "turbine_id", "diagnosis",
        "fault_severity", "fault_description", "recommended_actions"
    ]].head())

if __name__ == "__main__":
    main()