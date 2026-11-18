"""Generate frequency tables and a concise statistical summary."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "cleaned_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)
N = len(df)

columns = {
    "Year of study": "What is your current year of study?",
    "Gender": "What is your gender? (Optional)",
    "Primary transport mode": "What is your primary mode of transportation to college?",
    "Distance": "How far is your residence from college?",
    "Travel time": "How long does your daily journey to college usually take?",
    "Daily expenditure": "How much do you spend on transportation per day?",
    "Satisfaction rating": "How satisfied are you with your current mode of transportation?",
    "Commute problem": "What is the biggest problem you face during your commute?",
    "Public transport intention": "Would you consider using public transportation more often if it were cheaper and more reliable?"
}

tables = []
summary = [
    "STATISTICAL ANALYSIS SUMMARY",
    f"Number of valid response rows in the extracted dataset: {N}",
    f"Number of variables/columns: {df.shape[1]}",
    f"Missing cells in cleaned dataset: {int(df.isna().sum().sum())}",
    f"Duplicate rows in cleaned dataset: {int(df.duplicated().sum())}",
    "",
    "FREQUENCY DISTRIBUTIONS",
]
for label, column in columns.items():
    counts = df[column].value_counts(dropna=False)
    table = pd.DataFrame({
        "Variable": label,
        "Category": counts.index.astype(str),
        "Count": counts.values,
        "Percentage": (counts.values / N * 100).round(1)
    })
    tables.append(table)
    summary.append(f"\n{label}")
    for category, count in counts.items():
        summary.append(f"- {category}: {count} ({count/N*100:.1f}%)")

combined = pd.concat(tables, ignore_index=True)
combined.to_csv(OUT / "frequency_tables.csv", index=False)

sat_col = "How satisfied are you with your current mode of transportation?"
sat = pd.to_numeric(df[sat_col], errors="coerce").dropna()
summary += [
    "",
    "ORDINAL SATISFACTION SUMMARY",
    f"Mean satisfaction rating: {sat.mean():.2f} / 5",
    f"Median satisfaction rating: {sat.median():.1f} / 5",
    f"Standard deviation: {sat.std(ddof=1):.2f}",
    f"Ratings 4 or 5: {int(sat.isin([4, 5]).sum())} ({sat.isin([4, 5]).mean()*100:.1f}%)",
    "",
    "MULTI-SELECT FACTOR COUNTS",
    "Each factor is counted once per respondent. Percentages can sum to more than 100%.",
]
factor_col = "What is the most important factor when choosing transportation?"
factor_counts = {}
for answer in df[factor_col].dropna():
    for factor in set(p.strip() for p in str(answer).split(",") if p.strip()):
        factor_counts[factor] = factor_counts.get(factor, 0) + 1
for factor, count in sorted(factor_counts.items(), key=lambda x: x[1], reverse=True):
    summary.append(f"- {factor}: {count} ({count/N*100:.1f}%)")

summary += [
    "",
    "INTERPRETATION AND LIMITATIONS",
    "- This is a descriptive analysis of 45 response records reconstructed from a PDF.",
    "- The sample is highly concentrated in 2nd Year students; it is not representative",
    "  evidence for the entire college population.",
    "- Categorical survey answers are summarized using counts, percentages and cross-tabs.",
    "- Satisfaction is an ordinal 1-to-5 rating. Its mean is reported as a descriptive",
    "  summary only; the scale should not be treated as a precise continuous measurement.",
    "- No causal claims are made. No Pearson correlation matrix is calculated because",
    "  most fields are categorical and arbitrary numeric coding would be misleading.",
    "- The ambiguous answer 'I go to college through walking' in the commute-problem",
    "  field is retained as submitted and should be mentioned as a data-quality limitation.",
    "- 'Dont have' in the multi-select factor field is also retained as submitted.",
]
(OUT / "statistical_analysis.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
print("Saved frequency_tables.csv and statistical_analysis.txt")
