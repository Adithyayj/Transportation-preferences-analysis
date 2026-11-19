"""Collect a new survey response and predict public-transport intention."""
from transportation_analysis.train_model import (
    MODEL_PATH,
    load_model,
    predict_intention,
)

SATISFACTION_COLUMN = (
    "How satisfied are you with your current mode of transportation?"
)

QUESTIONS = (
    (
        "What is your current year of study?",
        "Current year of study (e.g. 2nd Year): ",
    ),
    (
        "What is your gender? (Optional)",
        "Gender (e.g. Female, Male, or another response): ",
    ),
    (
        "What is your primary mode of transportation to college?",
        "Primary transport mode (e.g. Walking, Public bus): ",
    ),
    (
        "How far is your residence from college?",
        "Distance from college (e.g. Less than 2 km): ",
    ),
    (
        "How long does your daily journey to college usually take?",
        "Usual travel time (e.g. Less than 15 minutes): ",
    ),
    (
        "How much do you spend on transportation per day?",
        "Daily transport cost (e.g. INR 0-30): ",
    ),
    (
        "What is the most important factor when choosing transportation?",
        "Transport-choice factors (e.g. Cost, Safety): ",
    ),
    (
        "How satisfied are you with your current mode of transportation?",
        "Satisfaction rating (1-5): ",
    ),
    (
        "What is the biggest problem you face during your commute?",
        "Biggest commute problem: ",
    ),
)


def _read_answer(prompt, input_fn, output_fn):
    while True:
        answer = input_fn(prompt).strip()
        if answer.casefold() == "quit":
            raise SystemExit("Prediction cancelled.")
        if answer:
            return answer
        output_fn("A response is required. Type 'quit' to cancel.")


def collect_response(input_fn=input, output_fn=print):
    """Prompt for all model features and validate the satisfaction rating."""
    output_fn("Enter a new response. Type 'quit' at any prompt to cancel.")
    response = {}
    for column, prompt in QUESTIONS:
        answer = _read_answer(prompt, input_fn, output_fn)
        if column == SATISFACTION_COLUMN:
            while answer not in {"1", "2", "3", "4", "5"}:
                output_fn("Enter a whole-number satisfaction rating from 1 to 5.")
                answer = _read_answer(prompt, input_fn, output_fn)
        response[column] = answer
    return response


def run_interactive_prediction(input_fn=input, output_fn=print, model_path=MODEL_PATH):
    """Load the saved model, collect answers, and display a prediction."""
    try:
        model = load_model(model_path)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Saved model not found at {model_path}. "
            "Run `python -m transportation_analysis.train_model` first."
        ) from error

    response = collect_response(input_fn=input_fn, output_fn=output_fn)
    result = predict_intention(model, response)[0]
    output_fn(f"\nPredicted public-transport intention: {result['prediction']}")
    output_fn("Estimated class probabilities:")
    for label, probability in sorted(
        result["probabilities"].items(), key=lambda item: item[1], reverse=True
    ):
        output_fn(f"- {label}: {probability:.1%}")
    output_fn("These probabilities are not calibrated.")
    return result


def main():
    run_interactive_prediction()


if __name__ == "__main__":
    main()
