import argparse
from pathlib import Path
from parser import (
    load_raw_transactions,
    normalize_transactions,
    compute_top_category
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart Financial Parser - normalize messy transactions."
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the raw transactions CSV file."
    )
    parser.add_argument(
        "--output", "-o", default="data/normalized.csv",
        help="Where to write the cleaned CSV."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    df = load_raw_transactions(input_path)
    clean_df = normalize_transactions(df)
    clean_df.to_csv(output_path, index=False)

    print("\n=== Cleaned Data Saved ===")
    print(f"Output: {output_path}")

    print("\n=== Spending Summary ===")
    if clean_df.empty:
        print("No valid spending data available.\n")
        return

    # Group by currency and compute stats per group
    for currency, group_df in clean_df.groupby("currency"):
        summary = compute_top_category(group_df)

        if summary["category"]:
            print(f"\nCurrency: {currency}")
            print(f" ▸ Top Category: {summary['category']}")
            print(f" ▸ Total Spent: {summary['total_spent']}")
        else:
            print(f"\nCurrency: {currency}")
            print(" ▸ No valid spending data in this currency")

    print()

if __name__ == "__main__":
    main()