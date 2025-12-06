from pathlib import Path
import pandas as pd

def load_raw_transactions(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def normalize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Normalize date formats
    - Standardize merchant names
    - Clean amount values
    """
    # TODO: implement step by step
    return df

def compute_top_category(df: pd.DataFrame) -> dict:
    """
    Return something like:
    {
        "category": "Food & Dining",
        "total_spent": 253.10
    }
    """
    # TODO: implement after categories are defined
    return {}
