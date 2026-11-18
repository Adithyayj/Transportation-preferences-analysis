# Analysis of Transportation Preferences and Travel Patterns Among College Students

This mini-project examines transportation choices, travel distance and time, daily expenditure, commute problems, and satisfaction among college students through a survey of 45 responses.

## Project team
- ADITHYA YJ (`NN25ISE012`)
- ANISH KA (`NN25ISE031`)
- ANIRUDH RK (`26DIPIS02`)

**Project Guide:** Dr. Vandana B S, Associate Professor

## Dataset
The repository includes 45 response records and 11 columns. `data/raw_data.csv` preserves the extracted source responses; `data/cleaned_data.csv` is produced by the cleaning script. The Google Form was not available for direct export, so the 45 rows were reconstructed from the supplied PDF of individual responses. The earlier report draft stated 42 responses and should be updated to reflect this dataset.

## Run
Python 3.9 or later:
```bash
pip install -r requirements.txt
python run_project.py
```
This runs cleaning, descriptive analysis, and statistical summaries. It creates 11 charts under `outputs/charts/` and frequency/cross-tabulation outputs in `outputs/`.

## Analysis scope
- Primary transport mode, year of study, and gender
- Travel distance, commute duration, and daily transport expenditure
- Satisfaction ratings and reported commute problems
- Willingness to use public transportation if it were cheaper and more reliable
- Transportation-choice factors (multi-select responses)
- Distance versus travel-time cross-tabulation

## Key observations
- Walking is the most common mode: 20 of 45 respondents (44.4%).
- Public bus is used by 12 respondents (26.7%).
- 21 respondents (46.7%) live less than 2 km from college.
- 19 respondents (42.2%) report a journey under 15 minutes.
- 29 respondents (64.4%) rate satisfaction as 4 or 5.
- 25 respondents (55.6%) would consider public transport more often if it were cheaper and more reliable; 15 (33.3%) answer Maybe.

## Cleaning and data-quality notes
- Trims leading/trailing whitespace and collapses repeated spaces.
- Standardizes gender capitalization and multi-select comma spacing.
- Does not infer respondent intent. `I go to college through walking` is retained in the commute-problem field as an inconsistent response. `Dont have` is retained in the factor field because its meaning is unclear.

## Limitations
- The sample is concentrated in 2nd Year students (41/45).
- Results describe these respondents and should not be generalized to all college students.
- Data was reconstructed from a response PDF, not exported directly from Google Forms.
- This is descriptive analysis and does not establish causation. A Pearson correlation heatmap is not used because most variables are categorical.

## Repository structure
```text
data/       raw_data.csv, cleaned_data.csv
src/        clean_data.py, generate_eda.py, statistical_analysis.py
outputs/    charts/, frequency_tables.csv, statistical_analysis.txt,
            distance_vs_travel_time.csv, data_quality_notes.txt
run_project.py
requirements.txt
```

**Academic integrity:** percentages and observations are calculated from the included 45-row dataset. No claim is made that the sample is random or representative.


## Automated run

GitHub Actions runs the analysis on pushes and pull requests targeting `main`. Each successful run stores the generated charts, tables and summary as an artifact named **`transportation-analysis-outputs`** for 14 days. Open the repository's **Actions** tab, select a successful run and download the artifact.
