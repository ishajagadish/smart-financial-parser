import pandas as pd
from pathlib import Path
from src.parser import (
    normalize_date,
    normalize_amount,
    normalize_merchant,
    apply_category,
    normalize_transactions
)
from datetime import datetime, timedelta


def test_normalize_date_valid():
    assert normalize_date("Jan 1st 23") == "2023-01-01"


def test_normalize_date_invalid():
    assert normalize_date("not-a-date") == "Unknown"


def test_normalize_amount():
    assert normalize_amount("$12.50") == 12.50
    assert normalize_amount("USD 5") == 5.0
    assert normalize_amount(None) == 0.0


def test_normalize_merchant_grouping():
    assert normalize_merchant("UBER *TRIP") == "Uber"
    assert apply_category("Uber") == "Transport"


def test_transaction_pipeline_drops_bad_rows():
    df = pd.DataFrame({
        "date": ["not-a-date", "2023-01-01"],
        "merchant": ["Unknown", "Starbucks #123"],
        "amount": ["$5.00", "$10.00"]
    })
    clean_df = normalize_transactions(df)
    assert len(clean_df) == 2
    assert clean_df.iloc[0]["date"] == "Unknown"
    assert clean_df.iloc[0]["merchant"] == "Unknown"

def test_normalize_date_yesterday():
    today = datetime.now()
    expected = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    assert normalize_date("yesterday") == expected

def test_normalize_date_next_friday():
    today = datetime.now()
    today_weekday = today.weekday()  # Monday=0 ... Sunday=6
    target = 4  # Friday
    
    diff = (target - today_weekday + 7) % 7
    if diff == 0:
        diff = 7
    expected = (today + timedelta(days=diff)).strftime("%Y-%m-%d")

    assert normalize_date("next Friday") == expected

def test_normalize_date_last_sunday():
    today = datetime.now()
    today_wd = today.weekday()
    target = 6  # Sunday

    diff = (today_wd - target + 7) % 7
    if diff == 0:
        diff = 7

    expected = (today - timedelta(days=diff)).strftime("%Y-%m-%d")

    assert normalize_date("last Sunday") == expected

def test_apply_category():
    assert apply_category("Uber") == "Transport"
    assert apply_category("Starbucks #1234") == "Food & Dining"
    assert apply_category("AMC Theatres") == "Entertainment"
    assert apply_category("Whole Foods Market") == "Grocery"
    assert apply_category("Random Boutique") == "Other"
