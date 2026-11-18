# Analysis of Transportation Preferences and Travel Patterns Among College Students

A mini-project that explores transportation choices, commuting patterns, daily travel expenditure, and satisfaction among college students using survey responses.

## Project team

- **ADITHYA YJ** (`NN25ISE012`)
- **ANISH KA** (`NN25ISE031`)
- **ANIRUDH RK** (`26DIPIS02`)

**Project Guide:** Dr. Vandana B S, Associate Professor

## Dataset

The repository contains 45 response records and 11 columns.

- `data/raw_data.csv`: extracted source responses, preserved without cleaning.
- `data/cleaned_data.csv`: whitespace and formatting standardized for analysis.

**Source note:** The original Google Form was not available for direct export. The response CSV was reconstructed from the supplied PDF of Google Form responses. The PDF contains 45 response records. An earlier report draft stated 42 responses, so its old statistics should be replaced with results generated from this dataset.

## Run the project

Python 3.9 or later is recommended.

```bash
pip install -r requirements.txt
python run_project.py
```

The pipeline:
1. Cleans `data/raw_data.csv` and recreates `data/cleaned_data.csv`.
2. Generates 11 descriptive charts in `outputs/charts/`.
3. Generates frequency tables and a statistical summary in `outputs/`.

You can also run each script separately:

```bash
python src/clean_data.py
python src/generate_eda.py
python src/statistical_analysis.py
```

## Main analysis

The project includes:
- Distribution of primary transportation modes.
- Year-of-study and gender distribution.
- Distance, travel-time and daily expenditure distributions.
- Satisfaction ratings.
- Reported commuting problems.
- Willingness to use public transportation if it becomes cheaper and more reliable.
- Multi-select transportation-choice factors.
- Distance versus travel-time cross-tabulation.

## Key observations from the 45 response records

- Walking is the most common primary mode: 20 respondents (44.4%).
- Public bus is next: 12 respondents (26.7%).
- 21 respondents (46.7%) live less than 2 km from college.
- 19 respondents (42.2%) report a journey under 15 minutes.
- 29 respondents (64.4%) rate satisfaction as 4 or 5.
- 25 respondents (55.6%) say they would consider public transport more often if it were cheaper and more reliable; another 15 (33.3%) answer Maybe.

See `outputs/statistical_analysis.txt` for detailed distributions.

## Data cleaning decisions

- Trimmed leading/trailing whitespace and collapsed repeated spaces.
- Standardized `male` / `female` capitalization.
- Standardized comma spacing and removed empty trailing entries in the multi-select factor field.
- Did not infer or rewrite respondent intent.
- The answer `I go to college through walking` appears in the commute-problem field and is retained as an ambiguous response.
- The factor answer `Dont have` is retained because its intended meaning cannot be confirmed.

## Limitations

- The sample is concentrated in 2nd Year students (41 of 45 responses).
- Findings describe these respondents only and should not be generalized to all college students.
- The dataset was reconstructed from a PDF rather than exported directly from the original form.
- The analysis is descriptive. It does not establish causation.
- Most variables are categorical, so a Pearson correlation heatmap is not appropriate without a defensible numeric encoding.

## Repository structure

```text
transportation-preferences-analysis/
├── data/
│   ├── raw_data.csv
│   └── cleaned_data.csv
├── src/
│   ├── clean_data.py
│   ├── generate_eda.py
│   └── statistical_analysis.py
├── outputs/
│   ├── charts/
│   ├── distance_vs_travel_time.csv
│   ├── frequency_tables.csv
│   └── statistical_analysis.txt
├── .gitignore
├── README.md
├── requirements.txt
└── run_project.py
```

## Academic integrity note

All percentages and observations in this repository are calculated from the included 45-row response dataset. Do not describe the responses as a random or representative sample unless the survey sampling method supports that claim.
