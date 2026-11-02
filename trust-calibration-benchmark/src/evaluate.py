import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

scripts = [
    "run_models.py",
    "judge.py",
    "metrics.py"
]

for script in scripts:
    print(f"\nRunning {script}...", flush=True)

    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "src" / script)],
        cwd=PROJECT_ROOT,
        check=True
    )

    print(f"{script} completed successfully!", flush=True)

print("\nEvaluation pipeline completed successfully!")