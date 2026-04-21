import json
from jsonschema import validate, ValidationError
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "prompts/planning/schema.json"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_plan(plan_dict):
    schema = load_schema()

    try:
        validate(instance=plan_dict, schema=schema)
        return True
    except ValidationError as e:
        raise Exception(f"❌ Invalid plan format: {e.message}")