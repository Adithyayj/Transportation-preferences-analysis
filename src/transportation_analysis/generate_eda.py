"""Generate descriptive charts and cross-tabulation for the survey."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed" / "cleaned_data.csv"
OUT = ROOT / "outputs" / "figures"
TABLES = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA)

C = {
    "year": "What is your current year of study?",
    "gender": "What is your gender? (Optional)",
    "mode": "What is your primary mode of transportation to college?",
    "distance": "How far is your residence from college?",
    "time": "How long does your daily journey to college usually take?",
    "cost": "How much do you spend on transportation per day?",
    "factors": "What is the most important factor when choosing transportation?",
    "satisfaction": "How satisfied are you with your current mode of transportation?",
    "problem": "What is the biggest problem you face during your commute?",
    "public": "Would you consider using public transportation more often if it were cheaper and more reliable?"
}


def categorical_chart(series, title, xlabel, filename, rotation=0):
    counts = series.value_counts(dropna=False)
    pct = counts / len(df) * 100
    use_horizontal = len(counts) >= 7 or max(map(len, counts.index.astype(str))) >= 20
    fig, ax = plt.subplots(figsize=(10, 6.5 if use_horizontal else 5.5))
    if use_horizontal:
        pct = pct.sort_values(ascending=True)
        bars = ax.barh(pct.index.astype(str), pct.values)
        ax.set_xlabel("Respondents (%)")
        ax.set_ylabel(xlabel)
        ax.grid(axis="x", alpha=.25)
        for bar, value in zip(bars, pct.values):
            ax.annotate(f"{value:.1f}%", (bar.get_width(), bar.get_y()+bar.get_height()/2),
                        xytext=(5, 0), textcoords="offset points", va="center", fontsize=8)
    else:
        bars = ax.bar(pct.index.astype(str), pct.values)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Respondents (%)")
        ax.tick_params(axis="x", rotation=rotation)
        if rotation:
            for label in ax.get_xticklabels():
                label.set_ha("right")
        ax.grid(axis="y", alpha=.25)
        for bar, value in zip(bars, pct.values):
            ax.annotate(f"{value:.1f}%", (bar.get_x()+bar.get_width()/2, bar.get_height()),
                        xytext=(0, 4), textcoords="offset points", ha="center", fontsize=8)
    ax.set_title(title, fontsize=13)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


categorical_chart(df[C["mode"]], "Primary Mode of Transportation", "Transport mode", "01_transport_modes.png", 25)
categorical_chart(df[C["year"]], "Respondents by Year of Study", "Year", "02_year_of_study.png")
categorical_chart(df[C["gender"]], "Respondents by Gender", "Gender", "03_gender.png")
categorical_chart(df[C["distance"]], "Distance from Residence to College", "Distance", "04_distance.png", 15)
categorical_chart(df[C["time"]], "Daily Travel Time to College", "Travel-time category", "05_travel_time.png", 15)
categorical_chart(df[C["cost"]], "Daily Transportation Expenditure", "Daily cost", "06_daily_cost.png", 15)
categorical_chart(df[C["satisfaction"]].astype(str).map(lambda x: f"Rating {x}"),
                  "Satisfaction with Current Transportation", "Rating", "07_satisfaction.png")
categorical_chart(df[C["problem"]], "Biggest Problems During Commute", "Reported problem", "08_commute_problems.png", 25)
categorical_chart(df[C["public"]], "Willingness to Use Public Transportation More Often", "Response", "09_public_transport_intention.png")

# Expand the multiple-selection question. Count each factor at most once per respondent.
factor_counts = {}
for answer in df[C["factors"]].dropna():
    # Count each selected factor once per respondent, preserving stable option order.
    for factor in dict.fromkeys(part.strip() for part in str(answer).split(",") if part.strip()):
        factor_counts[factor] = factor_counts.get(factor, 0) + 1
factor_series = pd.Series(factor_counts).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(factor_series.index, factor_series.values)
ax.set_title("Factors Considered When Choosing Transportation")
ax.set_xlabel("Factor")
ax.set_ylabel("Number of respondents")
ax.tick_params(axis="x", rotation=20)
for label in ax.get_xticklabels():
    label.set_ha("right")
ax.grid(axis="y", alpha=.25)
ax.set_axisbelow(True)
for bar, value in zip(bars, factor_series.values):
    ax.annotate(str(value), (bar.get_x()+bar.get_width()/2, bar.get_height()),
                xytext=(0, 4), textcoords="offset points", ha="center", fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "10_transport_choice_factors.png", dpi=180, bbox_inches="tight")
plt.close(fig)

cross = pd.crosstab(df[C["distance"]], df[C["time"]])
TABLES.mkdir(parents=True, exist_ok=True)
cross.to_csv(TABLES / "distance_vs_travel_time.csv")
ax = cross.plot(kind="bar", stacked=True, figsize=(9, 5.5))
ax.set_title("Travel Time by Distance from College")
ax.set_xlabel("Distance from residence to college")
ax.set_ylabel("Number of respondents")
ax.tick_params(axis="x", rotation=15)
ax.legend(title="Travel time", bbox_to_anchor=(1.02, 1), loc="upper left")
ax.grid(axis="y", alpha=.25)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(OUT / "11_distance_vs_travel_time.png", dpi=180, bbox_inches="tight")
plt.close()
print(f"Generated 11 charts in {OUT}")
