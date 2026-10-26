import sys
from pathlib import Path

from ollama_client import chat_with_model


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = PROJECT_ROOT / "sample_projects" / "average_bug.py"
MAX_FILE_SIZE = 200_000


def analyze_code_file(file_path):
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise ValueError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError("The selected path is not a file.")

    if path.suffix.lower() != ".py":
        raise ValueError("Only Python files are supported.")

    if path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File is too large. Maximum size is 200 KB.")

    code = path.read_text(encoding="utf-8")

    if not code.strip():
        raise ValueError("The selected file is empty.")

    prompt_parts = [
        "You are CodePilot AI, a Python debugging assistant.",
        "Analyze the supplied Python source code carefully.",
        "",
        f"Filename: {path.name}",
        "",
        "Tasks:",
        "1. Explain the purpose of the code.",
        "2. Identify confirmed bugs and potential edge cases separately.",
        "3. Explain why each confirmed bug occurs.",
        "4. Suggest minimal, correct fixes.",
        "5. Suggest tests for the identified issues.",
        "6. Do not invent bugs or claim you executed the code.",
        "7. Python integers have arbitrary precision.",
        "8. Do not recommend floor division when normal division is intended.",
        "9. If expected behaviour is unclear, explain the alternatives.",
        "",
        "SOURCE CODE START",
        code,
        "SOURCE CODE END",
        "",
        "Use these report sections:",
        "Purpose, Confirmed Bugs, Potential Edge Cases, Recommended Fixes, Tests.",
    ]

    prompt = "\n".join(prompt_parts)

    return chat_with_model(prompt)


if __name__ == "__main__":
    target_file = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else DEFAULT_FILE
    )

    print("CODEPILOT AI - FILE ANALYZER")
    print("=" * 35)
    print(f"File: {target_file}")

    try:
        report = analyze_code_file(target_file)

        print("\nANALYSIS REPORT")
        print("-" * 35)
        print(report)

    except (OSError, RuntimeError, ValueError) as error:
        print(f"\nAnalysis failed: {error}")