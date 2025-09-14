# Docify-AI

[
![PyPI - Version](https://img.shields.io/pypi/v/docify-ai.svg?style=flat-square)
](https://pypi.org/project/docify-ai/)
[
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docify-ai.svg?style=flat-square)
](https://pypi.org/project/docify-ai/)
[
![Downloads](https://static.pepy.tech/badge/docify-ai)
](https://pepy.tech/project/docify-ai)

An intelligent command-line interface (CLI) that leverages AI to automate documentation, testing, and project scaffolding for local software projects.

## Key Features

*   **AI-Powered Documentation Generation**: Automatically create detailed and domain-specific `README.md` files for any project.
*   **Automated Test Suite Generation**: Generate runnable `pytest` test files covering various scenarios.
*   **Dockerfile Generation**: Create optimized `Dockerfile`s for containerizing your applications.
*   **GitHub Actions Workflow Generation**: Develop `YAML` configurations for CI/CD pipelines.
*   **Project Scaffolding**: Bootstrap new Python projects with a predefined structure.
*   **Docstring Generation**: Automatically add PEP 257–compliant docstrings to Python functions, classes, and modules.
*   **Jupyter Notebook Generation**: Kickstart data analysis with a starter notebook including data loading, EDA, and model training pipelines.
*   **Model Card Generation**: Create `MODEL_CARD.md` for ML/AI projects, detailing model information, intended use, and ethical considerations.
*   **Flexible AI Clients**: Support for both Google Gemini and OpenAI GPT models.

## Installation

Docify-AI is available on PyPI and can be installed using `pip`:

```bash
pip install docify-ai
```

## Usage

The `docify` command is the entry point to all functionalities.

### 1. API Key Setup

Before using the tool, you must set your `GEMINI_API_KEY` or `OPENAI_API_KEY` as an environment variable. Alternatively, you can provide it directly via the `--key` argument.

```bash
# Example for Linux/macOS
export GEMINI_API_KEY='YOUR_GEMINI_API_KEY'

# Example for OpenAI
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
```

### 2. CLI Commands & Options

#### Global Options

These options can be used with any action:

*   `--path`, `-p`: Root directory of the project (default: current directory).
*   `--output`, `-o`: Custom output file/folder name.
*   `--client`, `-c`: AI client to use (`openai` or `gemini`, default: `gemini`).
*   `--key`, `-k`: Provide the API key directly, overriding environment variables.
*   `--ignore-dirs`: Space-separated list of directories to ignore.
*   `--ignore-exts`: Space-separated list of file extensions to ignore.

#### Command Examples

**Generate `README.md` (Default Action)**
Analyzes your project and creates a professional README file.

```bash
docify --path /path/to/your/project
```

**Generate Pytest Tests**
Creates a `tests/` directory with `pytest`-compatible test modules.

```bash
docify --test --path /path/to/your/project
```

**Generate a Dockerfile**
Creates a `Dockerfile` tailored to your project's needs.

```bash
docify --docker --path /path/to/your/project
```

**Generate a GitHub Actions Workflow**
Creates a `.github/workflows/ci.yml` file for continuous integration.

```bash
docify --gha --path /path/to/your/project
```

**Bootstrap a New Python Project**
Generates a basic Python project structure from a description.

```bash
docify --init "A simple Flask API for managing tasks"
```

**Add Docstrings to a Python File**
Inserts Google-style docstrings into a specified Python file in-place.

```bash
docify --docstring /path/to/your/project/my_module.py
```

**Generate a Jupyter Notebook**
Creates a starter Jupyter Notebook for data analysis or ML projects.

```bash
docify --notebook --path /path/to/your/data_project
```

**Generate a Model Card**
Creates a `MODEL_CARD.md` for your AI/ML projects.

```bash
docify --model-card --path /path/to/your/ml_project
```