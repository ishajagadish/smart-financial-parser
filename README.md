# Smart Financial Coach (PANW Case Study)

## Overview
Command-line tool that ingests a messy CSV of financial transactions, normalizes it, and reports the top spending category.

## How to Run
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

python src/main.py --input data/sample_raw.csv --output data/normalized.csv
