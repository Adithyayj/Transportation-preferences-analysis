"""Run the complete transportation survey analysis pipeline."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for script in ("src/clean_data.py", "src/generate_eda.py", "src/statistical_analysis.py"):
    print(f"\nRunning {script} ...")
    subprocess.run([sys.executable, str(ROOT / script)], check=True)
print("\nProject pipeline completed. See the outputs/ folder.")
