import tempfile
import unittest
from pathlib import Path

import pandas as pd

from transportation_analysis.train_model import (
    TARGET_COLUMN,
    load_model,
    predict_intention,
    train_model,
)
from transportation_analysis.predict import collect_response


class TrainModelTests(unittest.TestCase):
    def test_training_saves_model_and_predicts_unseen_categories(self):
        labels = ["Yes"] * 5 + ["Maybe"] * 5 + ["No"] * 5
        data = pd.DataFrame(
            {
                "Timestamp": [f"timestamp-{index}" for index in range(15)],
                "year": ["2nd Year"] * 15,
                "transport mode": ["Walking", "Bus", "Car"] * 5,
                TARGET_COLUMN: labels,
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "survey.csv"
            data.to_csv(data_path, index=False)
            train_model(data_path=data_path, output_dir=directory)

            model_path = (
                Path(directory)
                / "models"
                / "public_transport_intention_model.joblib"
            )
            self.assertTrue(model_path.exists())
            self.assertTrue((Path(directory) / "reports" / "model_evaluation.txt").exists())

            result = predict_intention(
                load_model(model_path),
                {"year": "unseen year", "transport mode": "unseen mode"},
            )[0]

        self.assertIn(result["prediction"], {"Yes", "Maybe", "No"})
        self.assertAlmostEqual(sum(result["probabilities"].values()), 1.0)

    def test_prediction_rejects_missing_required_features(self):
        bundle = {
            "feature_columns": ["year", "transport mode"],
            "model": None,
        }
        with self.assertRaisesRegex(ValueError, "Missing required model input columns"):
            predict_intention(bundle, {"year": "2nd Year"})

    def test_interactive_response_validates_satisfaction_rating(self):
        answers = iter(
            [
                "2nd Year",
                "Female",
                "Public bus",
                "5-10 km",
                "30-60 minutes",
                "31-60",
                "Cost, Safety",
                "6",
                "4",
                "Delays",
            ]
        )
        messages = []
        response = collect_response(
            input_fn=lambda prompt: next(answers),
            output_fn=messages.append,
        )

        self.assertEqual(len(response), 9)
        self.assertEqual(
            response["How satisfied are you with your current mode of transportation?"],
            "4",
        )
        self.assertTrue(
            any("rating from 1 to 5" in message for message in messages)
        )


if __name__ == "__main__":
    unittest.main()
