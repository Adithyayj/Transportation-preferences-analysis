"""Run the complete transportation survey analysis pipeline."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = (
    "src/clean_data.py",
    "src/generate_eda.py",
    "src/statistical_analysis.py",
)


def main():
    for script in SCRIPTS:
        print(f"\nRunning {script} ...", flush=True)
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)
    print("\nProject pipeline completed successfully. See the outputs/ folder.")


if __name__ == "__main__":
    main()
