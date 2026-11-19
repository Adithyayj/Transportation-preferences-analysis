"""Train and evaluate an exploratory public-transport-intention classifier."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed" / "cleaned_data.csv"
OUTPUT_DIR = ROOT / "outputs"
MODEL_PATH = OUTPUT_DIR / "models" / "public_transport_intention_model.joblib"
METRICS_PATH = OUTPUT_DIR / "reports" / "model_evaluation.txt"
TARGET_COLUMN = (
    "Would you consider using public transportation more often if it were "
    "cheaper and more reliable?"
)
EXCLUDED_COLUMNS = {"Timestamp", TARGET_COLUMN}
RANDOM_STATE = 42


def build_model():
    """Create a preprocessing and multiclass-classification pipeline."""
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def prepare_features(data, feature_columns=None):
    """Select predictors and treat survey responses as categorical values."""
    if feature_columns is None:
        feature_columns = [
            column for column in data.columns if column not in EXCLUDED_COLUMNS
        ]

    missing_columns = set(feature_columns) - set(data.columns)
    if missing_columns:
        raise ValueError(
            "Missing required model input columns: "
            + ", ".join(sorted(missing_columns))
        )
    if not feature_columns:
        raise ValueError("No predictor columns are available.")

    return data.loc[:, feature_columns].astype("string").fillna("Unknown")


def evaluate_model(features, target):
    """Compare stratified cross-validation macro F1 to a majority-class baseline."""
    class_counts = target.value_counts()
    if len(class_counts) < 2:
        raise ValueError("At least two target classes are required to train a model.")
    if class_counts.min() < 5:
        raise ValueError(
            "At least five examples per target class are required for "
            "5-fold stratified cross-validation."
        )

    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    model_scores = cross_val_score(
        build_model(), features, target, cv=folds, scoring="f1_macro"
    )
    baseline_scores = cross_val_score(
        DummyClassifier(strategy="most_frequent"),
        features,
        target,
        cv=folds,
        scoring="f1_macro",
    )
    return model_scores, baseline_scores


def load_model(path=MODEL_PATH):
    """Load the saved classifier bundle."""
    return joblib.load(path)


def predict_intention(model_bundle, responses):
    """Predict intention labels and class probabilities for one or more responses."""
    if isinstance(responses, dict):
        responses = pd.DataFrame([responses])
    elif not isinstance(responses, pd.DataFrame):
        raise TypeError("responses must be a dict or pandas DataFrame.")

    features = prepare_features(
        responses, feature_columns=model_bundle["feature_columns"]
    )
    probabilities = model_bundle["model"].predict_proba(features)
    labels = model_bundle["model"].classes_
    predictions = model_bundle["model"].predict(features)
    return [
        {
            "prediction": prediction,
            "confidence": float(probability.max()),
            "probabilities": {
                label: float(score) for label, score in zip(labels, probability)
            },
        }
        for prediction, probability in zip(predictions, probabilities)
    ]


def train_model(data_path=DATA, output_dir=OUTPUT_DIR):
    """Evaluate the model, fit on all rows, and save the model and report."""
    data = pd.read_csv(data_path)
    if data.empty:
        raise ValueError("The training dataset contains no response rows.")
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"Training data is missing target column: {TARGET_COLUMN}")

    data = data.dropna(subset=[TARGET_COLUMN])
    target = data[TARGET_COLUMN].astype("string")
    feature_columns = [
        column for column in data.columns if column not in EXCLUDED_COLUMNS
    ]
    features = prepare_features(data, feature_columns=feature_columns)
    model_scores, baseline_scores = evaluate_model(features, target)

    model = build_model()
    model.fit(features, target)
    model_bundle = {
        "model": model,
        "feature_columns": feature_columns,
        "target_column": TARGET_COLUMN,
    }

    output_dir = Path(output_dir)
    model_path = output_dir / "models" / MODEL_PATH.name
    metrics_path = output_dir / "reports" / METRICS_PATH.name
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_bundle, model_path)

    class_counts = target.value_counts()
    report = [
        "EXPLORATORY PUBLIC-TRANSPORT-INTENTION MODEL",
        f"Training responses: {len(data)}",
        f"Target classes: {len(class_counts)}",
        "Class counts:",
    ]
    report.extend(f"- {label}: {count}" for label, count in class_counts.items())
    report.extend(
        [
            "",
            "5-fold stratified cross-validation (macro F1):",
            (
                "Logistic regression: "
                f"{model_scores.mean():.3f} +/- {model_scores.std():.3f}"
            ),
            (
                "Most-frequent-class baseline: "
                f"{baseline_scores.mean():.3f} +/- {baseline_scores.std():.3f}"
            ),
            "",
            (
                f"Caution: only {len(data)} survey responses are available. "
                "These cross-validation"
            ),
            "scores are highly uncertain and are not evidence of population-level",
            "predictive performance. Output probabilities are not calibrated; use",
            "predictions for demonstration only.",
        ]
    )
    metrics_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Saved model: {model_path}")
    print(f"Saved evaluation: {metrics_path}")
    print("\n".join(report))
    return model_bundle, model_scores, baseline_scores


def main():
    train_model()


if __name__ == "__main__":
    main()
