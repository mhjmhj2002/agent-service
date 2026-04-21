from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    path = BASE_PATH / filename

    if not path.exists():
        raise Exception(f"Prompt file not found: {filename}")

    return path.read_text()