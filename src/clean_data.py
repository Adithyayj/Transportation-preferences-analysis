"""Clean the extracted survey CSV without changing response meaning."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw_data.csv"
OUTPUT = ROOT / "data" / "cleaned_data.csv"

def normalize_text(value):
    if pd.isna(value):
        return value
    return " ".join(str(value).strip().split())

def main():
    data = pd.read_csv(INPUT)
    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].map(normalize_text)

    gender = "What is your gender? (Optional)"
    if gender in data:
        data[gender] = data[gender].replace({"male": "Male", "female": "Female"})

    factors = "What is the most important factor when choosing transportation?"
    if factors in data:
        def normalize_multi_select(value):
            if pd.isna(value):
                return value
            parts = [part.strip() for part in str(value).split(",")]
            return ", ".join(part for part in parts if part)
        data[factors] = data[factors].map(normalize_multi_select)

    # Ambiguous answers are intentionally retained, not guessed or recoded.
    data.to_csv(OUTPUT, index=False)
    print(f"Saved {OUTPUT} ({len(data)} rows, {len(data.columns)} columns).")

if __name__ == "__main__":
    main()
