# Smart Financial Parser

A robust CLI tool that ingests messy financial transaction data and standardizes it into clean, structured insights.

This project solves the challenge of normalizing **inconsistent** transaction data:
- Human-written dates (`"yesterday"`, `"next Friday"`, `"3 weeks ago"`, `"Jan 1st 23"`)
- Messy currency formats (`"$12?"`, `"USD 5"`, `"10$"`)
- Noisy merchant strings (`"UBER *TRIP"`, `"AMZN Mktp US"`, missing values)
- Categorization into **meaningful spend types**

---

## Key Features

| Capability | Examples it can handle | Why it matters |
|----------|----------------------|----------------|
| Natural-language date parsing | `"last Sunday"`, `"in 2 days"`, `"next Friday"` | Human-friendly input support |
| Multi-format date parsing | `13.05.23`, `3-7-2023`, `April 2024` | Global support |
| Currency extraction | `$10`, `€5.4`, `INR 200`, `GBP 3.00` | Detects & preserves currency |
| Numeric normalization | `"$$5.00"` → `5.0` | Removes noise & symbols |
| Merchant normalization | `"UBER *TRIP"` → `Uber` | Enables grouping analytics |
| Category classification | Whole Foods → Grocery | Business insights enabled |
| Error-safe defaults | Invalid dates → `"Unknown"` | Reliable in messy real data |

⚙ Supported currencies today: **USD, EUR, INR, GBP, CAD**  (Easily extendable)

🛡️ Cybersecurity mindset: **Never drop data**, always preserve visibility.

Designed with data lineage & auditability in mind, essential for compliance-driven environments like cybersecurity and finance.

---

## 📊 Output Schema

| Column | Description |
|--------|-------------|
| `date` | Normalized YYYY-MM-DD or `"Unknown"` |
| `merchant` | Canonical merchant name |
| `normalized_amount` | Numeric spend value |
| `currency` | Extracted currency code |
| `category` | Rule-based spend classification |

## 📄 Sample Input/Output

### Sample Input (raw CSV)
```bash
date,merchant,amount

Yesterday,Uber Ride,$12?

last Sunday,,15.50

3-7-2023,AMZN Mktp US*AB12,$120.00

April 2024,MCDONALD’S #03944,20.00

2023/03/05,Starbucks ☕ Cafe, €5.4
```
### Sample Output
```bash
date,merchant,normalized_amount,currency,category

2025-12-04,Uber,12.0,USD,Transport

2025-11-30,Unknown,15.5,USD,Other

2023-03-07,Amazon,120.0,USD,Shopping

2024-04-01,McDonald's,20.0,USD,Food & Dining

2023-03-05,Starbucks,5.4,EUR,Food & Dining
```
## 📦 Installation

```bash
git clone https://github.com/<your-username>/smart-financial-parser.git
cd smart-financial-parser
pip3 install -r requirements.txt
```

## 🚀 Usage (CLI)
```bash
python3 src/main.py --input data/sample_raw.csv --output data/normalized.csv
```

## 🧪 Testing
```bash
python3 -m pytest -q
```

## 🔍 Top Spend Insight Output

CLI also prints Spending Summary, for ex:
```bash
Currency: USD
▸ Top category: Shopping
▸ Total Spent: 120.00
```
If multiple currencies exist, top spending is computed per currency and USD is reported by default for now (extendable).

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