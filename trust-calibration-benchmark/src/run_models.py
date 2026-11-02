
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# 1. Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "scenarios_final.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "responses"


# 2. Configuration
DRY_RUN = True
MAX_SCENARIOS = 1
MODEL_NAME = "openai/gpt-4o-mini"


# 3. Load API credentials
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# 4. Generate model response
def generate_response(prompt, model_name):
    """Generate a response from the selected model."""

    if DRY_RUN:
        return f"Test response from {model_name}"

    if model_name == "test_model":
        raise ValueError("Select a real model before making API requests.")

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    response = completion.choices[0].message.content

    if not response:
        raise ValueError("Model returned an empty response.")

    return response


# 5. Load scenarios
with open(DATA_PATH, "r", encoding="utf-8") as file:
    scenarios = json.load(file)

print("Loaded scenarios:", len(scenarios))


# 6. Prevent empty runs
if MAX_SCENARIOS == 0:
    print("No scenarios selected. Exiting without saving.")
    raise SystemExit(0)


# 7. Generate responses
results = []

for scenario in scenarios[:MAX_SCENARIOS]:
    result = {
        "scenario_id": scenario["id"],
        "model": MODEL_NAME,
        "run_id": 1,
        "response": generate_response(
            scenario["prompt"],
            MODEL_NAME
        )
    }

    results.append(result)

print("Total generated results:", len(results))


# 8. Save results
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if DRY_RUN:
    filename = "test_all_responses.json"
else:
    filename = "real_all_responses.json"

ALL_RESULTS_PATH = OUTPUT_DIR / filename

with open(ALL_RESULTS_PATH, "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print("Responses saved:", ALL_RESULTS_PATH)
