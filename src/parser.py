from pathlib import Path
import pandas as pd
import re
from datetime import datetime, timedelta
import dateparser as dp
from dateutil import parser as dateutil_parser

REFERENCE_DATE = datetime.now()  # ensures consistent relative parsing

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

# Simple merchant → category mapping
CATEGORY_MAP = {
    "uber": "Transport",
    "uber eats": "Food & Dining",
    "starbucks": "Food & Dining",
    "amazon": "Shopping",
}

def load_raw_transactions(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def normalize_date(date_str: str) -> str:
    if not isinstance(date_str, str) or not date_str.strip():
        return "Unknown"

    text = date_str.strip().lower()

    # Custom logic for "<modifier> <weekday>"
    parts = text.split()
    if len(parts) >= 2:
        modifier, weekday = parts[0], parts[1]
        if weekday in WEEKDAYS:
            today_idx = REFERENCE_DATE.weekday()
            target_idx = WEEKDAYS[weekday]

            if modifier == "next":
                diff = (target_idx - today_idx + 7) % 7
                if diff == 0:
                    diff = 7
                dt = REFERENCE_DATE + timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

            if modifier in {"last", "previous", "past"}:
                diff = (today_idx - target_idx + 7) % 7
                if diff == 0:
                    diff = 7
                dt = REFERENCE_DATE - timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

            if modifier == "this":
                diff = target_idx - today_idx
                dt = REFERENCE_DATE + timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

    # Natural language (+ require valid settings)
    dt = dp.parse(
        date_str,
        settings={
            "RELATIVE_BASE": REFERENCE_DATE,
            "PREFER_DATES_FROM": "past",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "STRICT_PARSING": True,
            "NORMALIZE": True,
        }
    )
    if dt:
        return dt.strftime("%Y-%m-%d")

    # Fallback parser for strict formats
    try:
        dt = dateutil_parser.parse(date_str, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"

def normalize_amount(value: str) -> float:
    if pd.isna(value):
        return 0.0
    s = re.sub(r"[^\d\-.]", "", str(value))  # strip currency symbols and spaces
    return float(s) if s else 0.0

def normalize_merchant(name: str) -> str:
    if not isinstance(name, str):
        return "Unknown"

    lower = name.lower()

    # Group messy naming into canonical merchants
    if "uber" in lower:
        if "eats" in lower:
            return "Uber Eats"
        return "Uber"
    if "starbucks" in lower:
        return "Starbucks"
    if "amzn" in lower or "amazon" in lower:
        return "Amazon"

    return name.title().strip()

def apply_category(merchant: str) -> str:
    lower = merchant.lower()
    for key, category in CATEGORY_MAP.items():
        if key in lower:
            return category
    return "Other"

def normalize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize each column
    df["date"] = df["date"].astype(str).apply(normalize_date)
    df["merchant"] = df["merchant"].apply(normalize_merchant)
    df["amount"] = df["amount"].apply(normalize_amount)

    # Add category
    df["category"] = df["merchant"].apply(apply_category)

    return df

def compute_top_category(df: pd.DataFrame) -> dict:
    # Only count positive spend
    spend_df = df[df["amount"] > 0]
    category_totals = spend_df.groupby("category")["amount"].sum()

    if category_totals.empty:
        return {"category": None, "total_spent": 0.0}

    top_category = category_totals.idxmax()
    total_spent = round(category_totals.max(), 2)

    return {"category": top_category, "total_spent": total_spent}
