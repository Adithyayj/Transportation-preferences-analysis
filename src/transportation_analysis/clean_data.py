"""Clean the extracted survey CSV without changing respondent meaning."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "raw" / "raw_data.csv"
OUTPUT = ROOT / "data" / "processed" / "cleaned_data.csv"
GENDER_COLUMN = "What is your gender? (Optional)"
FACTORS_COLUMN = "What is the most important factor when choosing transportation?"


def normalize_text(value):
    """Trim surrounding whitespace and collapse repeated spaces."""
    if pd.isna(value):
        return value
    return " ".join(str(value).strip().split())


def normalize_gender(value):
    """Standardize known gender labels and leave any other answer unchanged."""
    if pd.isna(value):
        return value
    normalized = normalize_text(value)
    known_values = {"male": "Male", "female": "Female"}
    return known_values.get(normalized.casefold(), normalized)


def normalize_multi_select(value):
    """Normalize comma spacing while preserving the original option wording."""
    if pd.isna(value):
        return value
    options = [normalize_text(part) for part in str(value).split(",")]
    # Keep each non-empty option once, preserving the respondent's option order.
    return ", ".join(dict.fromkeys(option for option in options if option))


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Raw survey data was not found: {INPUT}")

    data = pd.read_csv(INPUT, encoding="utf-8-sig")
    if data.empty:
        raise ValueError("The raw survey dataset contains no response rows.")

    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].map(normalize_text)

    if GENDER_COLUMN in data.columns:
        data[GENDER_COLUMN] = data[GENDER_COLUMN].map(normalize_gender)
    if FACTORS_COLUMN in data.columns:
        data[FACTORS_COLUMN] = data[FACTORS_COLUMN].map(normalize_multi_select)

    # Do not infer or rewrite ambiguous answers. They remain visible for review.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT, index=False, encoding="utf-8")
    print(f"Saved {OUTPUT} ({len(data)} rows, {len(data.columns)} columns).")


if __name__ == "__main__":
    main()
