import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart Financial Coach - normalize messy transactions."
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the raw transactions CSV file."
    )
    parser.add_argument(
        "--output",
        "-o",
        default="data/normalized.csv",
        help="Path to write the cleaned CSV."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    # TODO: call your normalization logic here
    print(f"[DEBUG] Would read: {input_path}")
    print(f"[DEBUG] Would write normalized data to: {args.output}")

if __name__ == "__main__":
    main()
