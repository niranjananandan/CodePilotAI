# CodePilot AI — Coding & Debugging Agent

CodePilot AI is a local AI-powered coding and debugging assistant built with Python and Ollama. It analyzes Python source files, identifies potential issues, generates proposed fixes, and runs automated tests to help verify code changes.

## Features

- **Project Inspector:** Lists Python files in the project.
- **AI Code Analysis:** Uses a local language model to review Python code.
- **AI Fix Generator:** Generates proposed code fixes and displays a diff before applying changes.
- **Human Approval:** Requires explicit approval before modifying a source file.
- **Backup Protection:** Creates a backup before applying a proposed fix.
- **Automated Testing:** Runs Python unit tests to check whether a proposed change passes the project's tests.
- **Failure Recovery:** Attempts to restore the original file if the automated tests fail.

## Technology Stack

- Python
- Ollama
- Qwen2.5-Coder 1.5B
- Python `unittest`
- Git

## Requirements

- Windows 11 or a compatible operating system
- Python 3.13 or a compatible Python version
- Git
- Ollama
- The `qwen2.5-coder:1.5b` model

## Setup

1. Install Python, Git, and Ollama.
2. Download the required model:

   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```

3. Ensure Ollama is running.
4. Open a terminal in the CodePilot AI project directory.

The project currently uses Python's standard library and does not require a separate Python package installation.

## Run CodePilot AI

From the project root, execute:

```bash
python src/agent.py
```

The interactive menu provides these options:

1. Inspect project files
2. Analyze a Python file
3. Run automated tests
4. Generate and apply an AI fix
5. Exit

## Run Tests

Run the project's unit tests with:

```bash
python -m unittest discover -s tests -v
```

Review the test output to determine whether the tests passed or failed.

## Project Structure

```text
CodePilotAI/
├── src/
│   ├── agent.py
│   ├── code_analyzer.py
│   ├── fix_generator.py
│   ├── ollama_client.py
│   ├── project_inspector.py
│   └── test_runner.py
├── tests/
├── sample_projects/
├── docs/
├── .gitignore
└── README.md
```

## Safety Notes

- Review proposed changes before approving them.
- Automated tests cannot guarantee that a code change is completely correct.
- Test execution runs Python code. Only run tests for projects you trust.
- Backups are created before proposed fixes are applied.
- AI-generated analysis and fixes may contain mistakes and should be reviewed.

## Current Status

The project currently supports project inspection, AI-assisted source analysis, proposed code fixes, approval-based file modification, and automated test execution.

## Future Improvements

- More reliable bug detection and verification
- Better handling of multi-file projects
- Improved error analysis and test generation
- A graphical user interface
- More detailed test and fix reports

## License

A license has not yet been selected. Add a suitable license before publishing the project for reuse.