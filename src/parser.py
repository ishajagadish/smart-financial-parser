from pathlib import Path
import pandas as pd
import re
from datetime import datetime, timedelta
import dateparser as dp
from dateutil import parser as dateutil_parser
import unicodedata

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

CATEGORY_RULES = {
    "Food & Dining": ["starbucks", "mcdonald's", "burger", "pizza", "restaurant", "cafe", "uber eats", "takeout", "doordash"],
    "Transport": ["uber", "lyft", "taxi", "gas", "shell", "chevron"],
    "Entertainment": ["amc", "spotify", "netflix", "theatre", "cinema", "bowling", "movies"],
    "Shopping": ["amazon", "walmart", "target", "best buy", "pacsun", "mall"],
    "Grocery": ["whole foods", "safeway", "kroger", "costco", "trader joe's"],
}

CURRENCY_PATTERNS = {
    "USD": [r"\$", r"usd"],
    "EUR": [r"€", r"eur", r"euro"],
    "INR": [r"₹", r"inr"],
    "GBP": [r"£", r"gbp"],
    "CAD": [r"cad", r"c\$"],   # NEW
}

def extract_currency_and_amount(raw_value: str):
    if raw_value is None or not isinstance(raw_value, str):
        return 0.0, "USD"

    text = raw_value.lower()
    currency = "USD"

    for curr, patterns in CURRENCY_PATTERNS.items():
        for p in patterns:
            if re.search(p, text):
                currency = curr
                break

    numeric = re.sub(r"[^\d\-.]", "", raw_value)
    amount = float(numeric) if numeric else 0.0
    return amount, currency


def normalize_amount(value: str) -> float:
    amount, _ = extract_currency_and_amount(value)
    return amount


def extract_currency(value: str) -> str:
    _, currency = extract_currency_and_amount(value)
    return currency


def load_raw_transactions(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def normalize_date(date_str: str) -> str:
    if not isinstance(date_str, str) or not date_str.strip():
        return "Unknown"

    text = date_str.strip().lower()
    parts = text.split()

    if len(parts) >= 2:
        modifier, weekday = parts[0], parts[1]
        if weekday in WEEKDAYS:
            today_idx = REFERENCE_DATE.weekday()
            target_idx = WEEKDAYS[weekday]

            if modifier == "next":
                diff = (target_idx - today_idx + 7) % 7 or 7
                dt = REFERENCE_DATE + timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

            if modifier in {"last", "previous", "past"}:
                diff = (today_idx - target_idx + 7) % 7 or 7
                dt = REFERENCE_DATE - timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

            if modifier == "this":
                diff = target_idx - today_idx
                dt = REFERENCE_DATE + timedelta(days=diff)
                return dt.strftime("%Y-%m-%d")

    dt = dp.parse(date_str, settings={
        "RELATIVE_BASE": REFERENCE_DATE,
        "PREFER_DATES_FROM": "past",
        "RETURN_AS_TIMEZONE_AWARE": False,
        "STRICT_PARSING": True,
        "NORMALIZE": True,
    })

    if dt:
        return dt.strftime("%Y-%m-%d")

    try:
        dt = dateutil_parser.parse(date_str, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"


def clean_merchant(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        return "unknown"

    name = name.lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    name = re.sub(r"[^a-z\s]", " ", name)
    return re.sub(r"\s+", " ", name).strip()


def normalize_merchant(name: str) -> str:
    cleaned = clean_merchant(name)

    if not cleaned or cleaned == "unknown":
        return "Unknown"

    if "uber eats" in cleaned:
        return "Uber Eats"
    if "uber" in cleaned:
        return "Uber"
    if "starbucks" in cleaned:
        return "Starbucks"
    if "amzn" in cleaned or "amazon" in cleaned:
        return "Amazon"
    if "mcdonald" in cleaned:
        return "McDonald's"
    if "trader joe" in cleaned:
        return "Trader Joe's"

    # Safe fallback: title-case the cleaned string
    return cleaned.title().strip()


def apply_category(merchant: str) -> str:
    lower = merchant.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(k in lower for k in keywords):
            return category
    return "Other"


def normalize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = df["date"].astype(str).apply(normalize_date)
    df["merchant"] = df["merchant"].apply(normalize_merchant)

    df["normalized_amount"] = df["amount"].apply(normalize_amount)
    df["currency"] = df["amount"].apply(extract_currency)

    df["category"] = df["merchant"].apply(apply_category)

    return df[["date", "merchant", "normalized_amount", "currency", "category"]]


def compute_top_category(df: pd.DataFrame) -> dict:
    spend_df = df[df["normalized_amount"] > 0]
    category_totals = spend_df.groupby("category")["normalized_amount"].sum()

    if category_totals.empty:
        return {"category": None, "total_spent": 0.0}

    top_category = category_totals.idxmax()
    total_spent = round(category_totals.max(), 2)
    return {"category": top_category, "total_spent": total_spent}