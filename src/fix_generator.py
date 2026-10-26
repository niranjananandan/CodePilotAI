
import ast
import difflib
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from ollama_client import chat_with_model
from test_runner import run_tests


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAX_FILE_SIZE_BYTES = 200_000


def request_requires_change(issue):
    pattern = (
        r"\b(fix|modify|change|add|implement|correct|repair|"
        r"handle|prevent|update|replace)\b"
    )
    return bool(re.search(pattern, issue, re.IGNORECASE))


def extract_code_blocks(response):
    return re.findall(
        r"```(?:python|py)?[ \t]*\r?\n(.*?)```",
        response,
        flags=re.IGNORECASE | re.DOTALL,
    )


def generate_candidate(file_path, issue):
    root = PROJECT_ROOT.resolve()
    target = Path(file_path).expanduser()

    if not target.is_absolute():
        target = root / target

    target = target.resolve()

    try:
        relative_path = target.relative_to(root)
    except ValueError as error:
        raise ValueError(
            "Only files inside the CodePilot project are allowed."
        ) from error

    if not target.is_file():
        raise ValueError(f"Python file not found: {relative_path}")

    if target.suffix.lower() != ".py":
        raise ValueError("Only Python files can be modified.")

    if target.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise ValueError("File is too large to process safely.")

    original_code = target.read_text(encoding="utf-8")

    if not original_code.strip():
        raise ValueError("The selected Python file is empty.")

    if not issue.strip():
        raise ValueError("Please describe the bug or requested fix.")

    prompt = f"""
You are CodePilot AI, a careful Python code editing engineer.

USER REQUEST:
{issue}

FILE:
{relative_path}

CURRENT SOURCE CODE:
```python
{original_code}
```

RULES:
1. Implement the requested behavior if it is missing or incorrect.
2. Preserve normal behavior and unrelated code.
3. Do not invent unrelated improvements.
4. Return the complete replacement Python file in exactly one
   Python code block.
5. If no change is necessary, return the original file unchanged
   inside one Python code block.
6. Never return NO_CHANGE as plain text.
7. Do not claim that you executed tests.
8. Do not include explanations outside the code block.
"""

    response = chat_with_model(prompt)
    code_blocks = extract_code_blocks(response)

    if not code_blocks and request_requires_change(issue):
        print(
            "\nThe AI did not provide a code change. "
            "Retrying once with a stricter instruction..."
        )

        retry_prompt = f"""
Your previous response did not provide a replacement file.

The user explicitly requests this change:
{issue}

The requested behavior must be implemented if it is not already present.

File: {relative_path}

Current source:
```python
{original_code}
```

Return the COMPLETE replacement Python file inside exactly one
Python code block. Do not return NO_CHANGE or an explanation.
Preserve unrelated behavior. Do not claim that you ran tests.
"""

        response = chat_with_model(retry_prompt)
        code_blocks = extract_code_blocks(response)

    if not code_blocks:
        if response.strip().upper() == "NO_CHANGE":
            if request_requires_change(issue):
                raise RuntimeError(
                    "The AI could not generate the explicitly requested "
                    "fix after retrying. No files were changed. "
                    "The model may be unable to follow this request reliably."
                )

            return target, original_code, original_code

        raise RuntimeError(
            "The AI did not return a complete Python code block. "
            "No files were changed."
        )

    if len(code_blocks) != 1:
        raise RuntimeError(
            "The AI returned multiple code blocks. "
            "No files were changed."
        )

    candidate_code = code_blocks[0].strip("\r\n") + "\n"

    try:
        ast.parse(candidate_code)
    except SyntaxError as error:
        raise RuntimeError(
            f"The proposed code contains a syntax error: {error}. "
            "No files were changed."
        ) from error

    return target, original_code, candidate_code


def show_diff(target, original_code, candidate_code):
    relative_path = target.relative_to(PROJECT_ROOT.resolve())

    diff = difflib.unified_diff(
        original_code.splitlines(),
        candidate_code.splitlines(),
        fromfile=str(relative_path),
        tofile=f"{relative_path} (proposed)",
        lineterm="",
    )

    changes = "\n".join(diff)

    if not changes:
        print("\nNo changes are necessary.")
        return False

    print("\nPROPOSED CHANGES")
    print("=" * 50)
    print(changes)

    return True


def apply_with_backup(target, original_code, candidate_code):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = target.with_name(f"{target.name}.{timestamp}.bak")

    shutil.copy2(target, backup_path)

    try:
        target.write_text(candidate_code, encoding="utf-8")

        print("\nRunning project tests to verify the fix...\n")
        report = run_tests(PROJECT_ROOT)

        if report["stdout"]:
            print(report["stdout"])

        if report["stderr"]:
            print(report["stderr"])

        if not report["success"]:
            target.write_text(original_code, encoding="utf-8")
            print("\nTESTS FAILED.")
            print("The original file has been restored.")
            print(f"Backup: {backup_path}")
            return

        print("\nALL TESTS PASSED.")
        print("The proposed fix has been kept.")
        print(f"Original backup: {backup_path}")

    except Exception as error:
        try:
            target.write_text(original_code, encoding="utf-8")
            print("\nThe operation failed.")
            print("The original file has been restored.")
            print(f"Backup: {backup_path}")
        except OSError as restore_error:
            print("\nAutomatic restoration failed.")
            print(f"Backup available at: {backup_path}")
            print(f"Restoration error: {restore_error}")

        print(f"Details: {error}")


def main():
    target_argument = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "sample_projects/buggy_example.py"
    )

    issue = input(
        "Describe the bug or fix you want CodePilot to investigate: "
    ).strip()

    try:
        target, original_code, candidate_code = generate_candidate(
            target_argument,
            issue,
        )

        has_changes = show_diff(
            target, original_code, candidate_code
        )

        if not has_changes:
            return

        print("\nReview the proposed changes carefully.")
        confirmation = input(
            "Type APPLY to approve these changes, "
            "or anything else to cancel: "
        ).strip()

        if confirmation != "APPLY":
            print("\nCancelled. No files were changed.")
            return

        apply_with_backup(
            target, original_code, candidate_code
        )

    except (OSError, RuntimeError, ValueError) as error:
        print(f"\nFix generation failed: {error}")


if __name__ == "__main__":
    main()
