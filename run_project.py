"""Run the complete transportation survey analysis pipeline."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = (
    "transportation_analysis.clean_data",
    "transportation_analysis.generate_eda",
    "transportation_analysis.statistical_analysis",
    "transportation_analysis.train_model",
)


def main():
    for module in MODULES:
        print(f"\nRunning {module} ...", flush=True)
        subprocess.run(
            [sys.executable, "-m", module],
            check=True,
            cwd=ROOT,
        )
    print("\nProject pipeline completed successfully. See the outputs/ folder.")


if __name__ == "__main__":
    main()
