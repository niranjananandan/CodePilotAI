
import sys
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
}


def list_python_files(project_root, max_files=200):
    root = Path(project_root).expanduser().resolve()

    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")

    python_files = []

    for path in root.rglob("*.py"):
        relative_path = path.relative_to(root)

        if any(
            part in EXCLUDED_DIRECTORIES
            for part in relative_path.parts[:-1]
        ):
            continue

        if not path.is_file():
            continue

        python_files.append(relative_path.as_posix())

        if len(python_files) >= max_files:
            break

    return sorted(python_files)


if __name__ == "__main__":
    project_root = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent.parent / "sample_projects"
    )

    try:
        files = list_python_files(project_root)

        print("CODEPILOT AI - PROJECT INSPECTOR")
        print("=" * 35)
        print(f"Project: {project_root.resolve()}")
        print(f"Python files found: {len(files)}")

        for filename in files:
            print(f"  - {filename}")

    except (OSError, ValueError) as error:
        print(f"Inspection failed: {error}")
