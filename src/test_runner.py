import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_tests(project_root=PROJECT_ROOT, timeout_seconds=60):
    root = Path(project_root).resolve()
    tests_folder = root / "tests"

    if not root.is_dir():
        raise ValueError(f"Project folder not found: {root}")

    if not tests_folder.is_dir():
        raise ValueError(f"Tests folder not found: {tests_folder}")

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": f"Tests exceeded the {timeout_seconds}-second timeout.",
        }


if __name__ == "__main__":
    print("CODEPILOT AI - TEST RUNNER")
    print("=" * 35)

    try:
        report = run_tests()

        if report["stdout"]:
            print(report["stdout"])

        if report["stderr"]:
            print(report["stderr"])

        if report["success"]:
            print("RESULT: ALL TESTS PASSED")
        else:
            print("RESULT: TESTS FAILED")

    except (OSError, ValueError) as error:
        print(f"Test execution error: {error}")