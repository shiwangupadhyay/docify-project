# Docify-AI

An intelligent command-line interface (CLI) that leverages AI to automate documentation, testing, and project scaffolding for local software projects.

[![PyPI - Version](https://img.shields.io/pypi/v/docify-ai.svg?style=flat-square)](https://pypi.org/project/docify-ai/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docify-ai.svg?style=flat-square)](https://pypi.org/project/docify-ai/)
[![Downloads](https://static.pepy.tech/badge/docify-ai)](https://pepy.tech/project/docify-ai)


## Key Features

*   **AI-Powered Documentation Generation**: Automatically create detailed and domain-specific `README.md` files for any project.
*   **Automated Test Suite Generation**: Generate runnable `pytest` test files covering various scenarios.
*   **Dockerfile Generation**: Create optimized `Dockerfile`s for containerizing your applications.
*   **GitHub Actions Workflow Generation**: Develop `YAML` configurations for CI/CD pipelines (e.g., build, test, deploy).
*   **Project Scaffolding**: Bootstrap new Python projects with a predefined structure.
*   **Docstring Generation**: Automatically add PEP 257–compliant docstrings to Python functions, classes, and modules.
*   **Jupyter Notebook Generation**: Kickstart data analysis or ML projects with a basic Jupyter Notebook including data loading, EDA, and model training/evaluation pipelines.
*   **Model Card Generation**: Create `MODEL_CARD.md` for ML/AI projects, detailing model information, intended use, datasets, and ethical considerations.
*   **Flexible AI Clients**: Support for both Google Gemini and OpenAI GPT models.
*   **Intelligent File Scanning**: Ignores specified directories and file extensions to focus on relevant code.
*   **Dataset Schema Extraction**: Automatically infers schema and samples from common data formats (`.csv`, `.json`, etc.) to inform AI generations for data-centric tasks.


## Installation

Docify-AI can be installed directly from PyPI using `pip`:

```bash
pip install docify-ai
```

## Usage

The `docify` command is your entry point to all functionalities.

### API Key Setup

You must set your `GEMINI_API_KEY` or `OPENAI_API_KEY` environment variable or provide it via the `--key` argument.

```bash
# Example for setting environment variable (Linux/macOS)
export GEMINI_API_KEY='YOUR_GEMINI_API_KEY'
# or for OpenAI
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
```

### Global Options

*   `--path`, `-p`: Root directory of the project (default: current directory `.` ).
*   `--output`, `-o`: Custom output file/folder name.
*   `--client`, `-c`: Choose AI client (`openai` or `gemini`, default: `gemini`). Case-insensitive.
*   `--key`, `-k`: Provide API key directly (overrides environment variable).
*   `--ignore-dirs`: Space-separated list of directories to ignore during scanning.
*   `--ignore-exts`: Space-separated list of file extensions to ignore during scanning.

### CLI Commands

#### 1. Generate `README.md` (Default Action)

If no specific action flag is provided, `docify` generates a `README.md` for the project.

```bash
docify -p /path/to/your/project
# Output will be saved to /path/to/your/project/README.md
```

#### 2. Generate Pytest Test Files

Creates a `tests/` directory with `pytest` compatible test modules.

```bash
docify --test -p /path/to/your/project
# Output: tests/ directory within your project, e.g., tests/test_main.py
```

#### 3. Generate Dockerfile

Creates a `Dockerfile` for your project.

```bash
docify --docker -p /path/to/your/project
# Output: Dockerfile within your project
```

#### 4. Generate GitHub Actions Workflow

Creates a `.github/workflows/ci.yml` file for CI/CD.

```bash
docify --gha -p /path/to/your/project
# Output: .github/workflows/ci.yml within your project
```

#### 5. Bootstrap a New Python Project

Generates a basic Python project structure.

```bash
docify --init my_new_project
# Output: A new directory named 'my_new_project' with basic Python project files.
```

#### 6. Add Docstrings to a Python File

Inserts Google-style docstrings into a specified Python file.

```bash
docify --docstring /path/to/your/project/my_module.py
# The specified Python file will be updated in place.
```

#### 7. Generate a Jupyter Notebook

Creates a starter Jupyter Notebook, especially useful for data-centric projects.

```bash
docify --notebook -p /path/to/your/data_project
# Output: notebook.ipynb within your project.
```

#### 8. Generate a Model Card

Creates a `MODEL_CARD.md` for AI/ML projects.

```bash
docify --model-card -p /path/to/your/ml_project
# Output: MODEL_CARD.md within your project.
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes and new features.

## License

This project is licensed under the terms of the [MIT License](LICENSE).