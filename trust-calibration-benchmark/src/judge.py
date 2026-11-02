
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from validation import validate_judgment


# 1. Project configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DRY_RUN = True
JUDGE_MODEL = "openai/gpt-4o-mini"


# 2. Load judge instructions
JUDGE_PROMPT_PATH = (
    PROJECT_ROOT / "evaluation" / "judge_prompt_v1.md"
)

with open(JUDGE_PROMPT_PATH, "r", encoding="utf-8") as file:
    JUDGE_PROMPT = file.read()

print("Judge prompt loaded successfully!")


# 3. Configure OpenRouter
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key and not DRY_RUN:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

client = None

if not DRY_RUN:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )


# 4. Load model responses
RESPONSES_PATH = (
    PROJECT_ROOT / "outputs" / "responses" / "real_all_responses.json"
)

with open(RESPONSES_PATH, "r", encoding="utf-8") as file:
    responses = json.load(file)

print("Loaded responses:", len(responses))


# 5. Load benchmark scenarios
SCENARIOS_PATH = (
    PROJECT_ROOT / "data" / "scenarios_final.json"
)

with open(SCENARIOS_PATH, "r", encoding="utf-8") as file:
    scenarios = json.load(file)

scenario_lookup = {
    scenario["id"]: scenario["prompt"]
    for scenario in scenarios
}

print("Loaded scenarios:", len(scenario_lookup))


# 6. Configure output paths
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "evaluations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

prefix = "test" if DRY_RUN else "real"

ALL_JUDGMENTS_PATH = (
    OUTPUT_DIR / f"{prefix}_all_judgments.json"
)

ERRORS_PATH = (
    OUTPUT_DIR / f"{prefix}_judge_errors.json"
)

RAW_JUDGMENTS_PATH = (
    OUTPUT_DIR / f"{prefix}_raw_judgments.jsonl"
)


# 7. Save JSON safely
def save_json_safely(path, data):
    """Save JSON using a temporary file and atomic replacement."""

    temporary_path = path.with_suffix(".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    os.replace(temporary_path, path)


# 8. Save original judge response
def save_raw_judgment(raw_text, scenario_id, model, run_id):
    """Append the original judge response to a JSONL audit log."""

    record = {
        "scenario_id": scenario_id,
        "model": model,
        "run_id": run_id,
        "judge_model": JUDGE_MODEL,
        "raw_judgment": raw_text
    }

    with open(RAW_JUDGMENTS_PATH, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(record, ensure_ascii=False) + "\n"
        )


# 9. Judge function
def judge_response(
    scenario_prompt,
    model_response,
    scenario_id,
    response_model,
    run_id
):
    """Evaluate a model response using an LLM judge."""

    if DRY_RUN:
        judgment = {
            "primary_request_identified": "Test primary request",
            "observed_confidence": "not_assessable",
            "observed_behaviors": [],
            "unnecessary_behaviors": [],
            "unnecessary_behavior_rationales": {},
            "explicit_refusal": False,
            "harmful_assistance": False,
            "unjustified_refusal": False,
            "flag_for_review": False,
            "review_reason": None,
            "judge_rationale": "Test judgment only."
        }
        save_raw_judgment(
            raw_text=json.dumps(judgment),
            scenario_id=scenario_id,
            model=response_model,
            run_id=run_id
        )
        return validate_judgment(judgment)

    completion = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[
            {
                "role": "system",
                "content": JUDGE_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"Original scenario:\n{scenario_prompt}\n\n"
                    f"Model response:\n{model_response}"
                )
            }
        ],
        response_format={"type": "json_object"}
    )

    raw_judgment = completion.choices[0].message.content

    # Save raw output before parsing or validation
    save_raw_judgment(
        raw_text=raw_judgment,
        scenario_id=scenario_id,
        model=response_model,
        run_id=run_id
    )

    judgment = json.loads(raw_judgment)

    return validate_judgment(judgment)


# 10. Load previous progress
def load_json_list(path):
    """Load previously saved results, if available."""

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list in {path}")

    return data


judgments = load_json_list(ALL_JUDGMENTS_PATH)
failed_judgments = load_json_list(ERRORS_PATH)

print("Previously saved judgments:", len(judgments))


# 11. Identify completed responses
completed_keys = {
    (item["scenario_id"], item["model"], item["run_id"])
    for item in judgments
}


# 12. Evaluate remaining responses
for response in responses:
    scenario_id = response["scenario_id"]

    response_key = (
        scenario_id,
        response["model"],
        response["run_id"]
    )

    if response_key in completed_keys:
        print(f"Skipping already evaluated scenario {scenario_id}")
        continue

    try:
        judgment = judge_response(
            scenario_prompt=scenario_lookup[scenario_id],
            model_response=response["response"],
            scenario_id=scenario_id,
            response_model=response["model"],
            run_id=response["run_id"]
        )

        judgment["scenario_id"] = scenario_id
        judgment["model"] = response["model"]
        judgment["run_id"] = response["run_id"]

        judgments.append(judgment)
        completed_keys.add(response_key)

        # Remove old errors after successful evaluation
        failed_judgments = [
            item for item in failed_judgments
            if (
                item["scenario_id"],
                item["model"],
                item["run_id"]
            ) != response_key
        ]

    except Exception as error:
        # Keep only the latest error for this response
        failed_judgments = [
            item for item in failed_judgments
            if (
                item["scenario_id"],
                item["model"],
                item["run_id"]
            ) != response_key
        ]

        failed_judgments.append({
            "scenario_id": scenario_id,
            "model": response["model"],
            "run_id": response["run_id"],
            "error": str(error)
        })

        print(
            f"Judgment failed for scenario {scenario_id}: {error}"
        )

    # Save progress after every attempted evaluation
    save_json_safely(ALL_JUDGMENTS_PATH, judgments)
    save_json_safely(ERRORS_PATH, failed_judgments)


# 13. Save final results
save_json_safely(ALL_JUDGMENTS_PATH, judgments)
save_json_safely(ERRORS_PATH, failed_judgments)

print("Successful judgments:", len(judgments))
print("Failed judgments:", len(failed_judgments))
print("All judgments saved:", ALL_JUDGMENTS_PATH.exists())
print("Errors saved:", ERRORS_PATH.exists())
