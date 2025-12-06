# Smart Financial Data Normalizer

A robust CLI tool that ingests messy financial transaction data and standardizes it into clean, structured insights.

This project solves the challenge of normalizing **inconsistent** transaction data:
- Human-written dates (`"yesterday"`, `"next Friday"`, `"3 weeks ago"`, `"Jan 1st 23"`)
- Messy currency formats (`"$12?"`, `"USD 5"`, `"10$"`)
- Noisy merchant strings (`"UBER *TRIP"`, `"AMZN Mktp US"`, missing values)
- Categorization into **meaningful spend types**

---

## Features

| Capability | Examples | Benefit |
|----------|-----------|---------|
| Natural-language date parsing | "last Sunday", "in 2 days" | End-user friendly inputs |
| Multi-format date parsing | `13.05.23`, `3-7-2023` | International support |
| Currency cleaning | `$12?` → `12.0` | Removes noise safely |
| Merchant normalization | "UBER *TRIP" → "Uber" | Canonical grouping for analytics |
| Auto-category mapping | Uber → Transport | Immediate insights |
| Safe handling of malformed data | Unknown fields preserved | No crashes, auditable pipeline |

🛡️ Cybersecurity mindset: **Never drop data**, always preserve visibility.

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/smart-financial-parser.git
cd smart-financial-parser
pip3 install -r requirements.txt
```

## 🚀 Usage (CLI)
```bash
python3 src/main.py --input data/sample_raw.csv --output data/output_normalized.csv
```

## 🧪 Testing
```bash
python3 -m pytest -q
```

## 🔍 Top Spend Insight Output

CLI also prints Spending Summary, for ex:
```bash
Top category: Shopping
Total Spent: $120.00
```

## 🧠 Methodology

### Tools Used:

- Python 3.9
- Pandas — CSV ingestion & tabular cleaning
- dateparser — human-language date parsing
- dateutil — fallback multi-format parsing
- Regex — currency sanitation
- Pytest — automated verification of results

### How Output Was Verified

Built a stress-test dataset (sample_raw.csv) containing:

- relative dates
- mixed international formats
- malformed currency
- missing merchant/date fields
- corrupted rows

Wrote automated unit tests to confirm:

- Accurate normalization where possible
- "Unknown" fallback for invalid fields
- No pipeline crashes under messy input
- Manual inspection of before/after sample files
- Validated business logic via CLI execution

### AI Usage Disclosure

ChatGPT was used to accelerate:

- boilerplate generation
- documentation drafting
- test case brainstorming


I reviewed and validated every function and decision.
I fixed edge cases manually after iterative debugging.
I fully understand and take responsibility for all code.