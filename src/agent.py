
from pathlib import Path

from code_analyzer import analyze_code_file
from fix_generator import (
    apply_with_backup,
    generate_candidate,
    show_diff,
)
from project_inspector import list_python_files
from test_runner import run_tests


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def show_python_files():
    files = list_python_files(PROJECT_ROOT)

    print("\nCODEPILOT AI - PROJECT FILES")
    print("=" * 35)

    if not files:
        print("No Python files found.")
        return []

    for index, filename in enumerate(files, start=1):
        print(f"{index}. {filename}")

    return files


def select_python_file(files):
    choice = input("\nEnter the file number: ").strip()

    try:
        index = int(choice) - 1
    except ValueError:
        print("Invalid input. Enter a number from the list.")
        return None

    if index < 0 or index >= len(files):
        print("Invalid file number.")
        return None

    target_file = (PROJECT_ROOT / files[index]).resolve()

    try:
        target_file.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        print("Access denied: the file is outside the project folder.")
        return None

    return target_file


def analyze_selected_file(files):
    target_file = select_python_file(files)

    if target_file is None:
        return

    print(f"\nAnalyzing: {target_file.relative_to(PROJECT_ROOT)}")
    print("The AI is reviewing the code. Please wait...\n")

    try:
        report = analyze_code_file(target_file)

        print("=" * 50)
        print("CODEPILOT AI - ANALYSIS REPORT")
        print("=" * 50)
        print(report)

    except (OSError, RuntimeError, ValueError) as error:
        print(f"Analysis failed: {error}")


def execute_project_tests():
    print("\nProject tests will execute Python code.")
    confirmation = input("Run tests now? (y/n): ").strip().lower()

    if confirmation != "y":
        print("Test execution cancelled.")
        return

    print("\nRunning automated tests...\n")

    try:
        report = run_tests(PROJECT_ROOT)

        if report["stdout"]:
            print(report["stdout"])

        if report["stderr"]:
            print(report["stderr"])

        if report["success"]:
            print("RESULT: ALL TESTS PASSED")
        else:
            print("RESULT: TESTS FAILED")

    except (OSError, ValueError) as error:
        print(f"Test execution failed: {error}")


def generate_and_apply_fix(files):
    target_file = select_python_file(files)

    if target_file is None:
        return

    issue = input(
        "\nDescribe the bug or fix in one line: "
    ).strip()

    if not issue:
        print("No issue provided. Cancelled.")
        return

    print("\nGenerating a proposed fix...")
    print("Please wait; the original file will not be changed yet.")

    try:
        target, original_code, candidate_code = generate_candidate(
            target_file, issue
        )

        has_changes = show_diff(
            target, original_code, candidate_code
        )

        if not has_changes:
            print("No changes are necessary.")
            return

        print("\nReview the proposed changes carefully.")
        confirmation = input(
            'Type APPLY to approve these changes, or anything else to cancel: '
        ).strip()

        if confirmation != "APPLY":
            print("Cancelled. No files were changed.")
            return

        apply_with_backup(
            target, original_code, candidate_code
        )

    except (OSError, RuntimeError, ValueError) as error:
        print(f"Fix generation failed: {error}")


def main():
    while True:
        print("\n" + "=" * 45)
        print("             CODEPILOT AI")
        print("       Coding & Debugging Agent")
        print("=" * 45)
        print("1. Inspect project files")
        print("2. Analyze a Python file")
        print("3. Run automated tests")
        print("4. Generate and apply AI fix")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            show_python_files()

        elif choice == "2":
            files = show_python_files()
            if files:
                analyze_selected_file(files)

        elif choice == "3":
            execute_project_tests()

        elif choice == "4":
            files = show_python_files()
            if files:
                generate_and_apply_fix(files)

        elif choice == "5":
            print("CodePilot AI closed.")
            break

        else:
            print("Invalid option. Choose 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()
