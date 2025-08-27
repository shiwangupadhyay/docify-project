# Docify AI 🚀: Intelligent Documentation & Test Generation for Your Code

[![PyPI - Version](https://img.shields.io/pypi/v/docify-ai.svg?style=flat-square)](https://pypi.org/project/docify-ai/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/docify-ai.svg?style=flat-square)](https://pypi.org/project/docify-ai/)
[![Downloads](https://static.pepy.tech/badge/docify-ai)](https://pepy.tech/project/docify-ai)

A versatile AI-powered command-line tool for instantly generating comprehensive `README.md` files, pytest tests, Dockerfiles, and GitHub Actions CI/CD workflows for your local projects, powered by Google Gemini and OpenAI GPT models.


## Key Features ✨

*   **🤖 AI-Powered Content Generation**: Leverages large language models (Google Gemini and OpenAI GPT) to write human-quality `README.md` files, `pytest` tests, `Dockerfile`s, and GitHub Actions CI/CD workflows.
*   **💡 Versatile Output Formats**: Generate comprehensive project documentation, runnable unit tests, containerization configurations, or automation workflows.
*   **📂 Intelligent Project Analysis**: Scans your project directory, intelligently ignoring irrelevant files and directories (configurable with `--ignore-dirs` and `--ignore-exts`), to deeply understand its purpose, technologies, and structure.
*   **⚙️ Flexible AI Client Selection**: Seamlessly choose between Google Gemini and OpenAI GPT models for content generation directly from the command line.
*   **🔑 Robust API Key Management**: Supports API keys via environment variables or direct command-line arguments for both Gemini and OpenAI for enhanced security and convenience.
*   **🚀 Fast Project Scaffolding**: Bootstrap new Python projects with an intelligent, AI-generated initial structure using the `--init` option.
*   **⏱️ Rapid Generation**: Transform a nascent project or an existing codebase into a fully documented, tested, and deployable application in moments.
*   **🔧 Highly Customizable**: Specify project paths, output file names, and tailor content generation with various command-line options.


## Installation 📦

Docify-AI is available on PyPI and can be installed on any system with Python 3.8 or newer using `pip`.

```bash
pip install docify-ai
```

## Usage 🚀

Using Docify-AI is straightforward, involving a one-time API key setup and a simple command execution.

### 1. Set Your API Key

Docify-AI requires an API key for the chosen AI model (Google Gemini or OpenAI). You can obtain a free key from [Google AI Studio](https://aistudio.google.com/app/apikey) for Gemini, or from the [OpenAI platform](https://platform.openai.com/api-keys) for OpenAI.

Once you have your key, set it as an environment variable:

*   For **Google Gemini**: `GEMINI_API_KEY`
*   For **OpenAI**: `OPENAI_API_KEY`

**For macOS / Linux (bash/zsh):**

```bash
export GEMINI_API_KEY='your-gemini-secret-api-key'
# OR
export OPENAI_API_KEY='your-openai-secret-api-key'
```
*(To make this permanent across terminal sessions, add the line to your shell's configuration file, e.g., `~/.zshrc` or `~/.bashrc`.)*

**For Windows (PowerShell):**

```powershell
$Env:GEMINI_API_KEY="your-gemini-secret-api-key"
# OR
$Env:OPENAI_API_KEY="your-openai-secret-api-key"
```

Alternatively, you can pass the API key directly via the `--key` argument, which will override the environment variable.

### 2. Run Docify-AI

Navigate to the root directory of the project you wish to document and simply run the `docify` command. By default, it uses the Gemini model to generate a README.

```bash
docify
```
The tool will scan the current directory and generate a `README.md` file with AI-powered content.

### Command-Line Options

You can customize the behavior of Docify-AI using the following command-line arguments:

*   **`--path <directory>` / `-p <directory>`**: Specifies the root directory of the project to be analyzed. Defaults to the current working directory (`.`).
*   **`--output <filename_or_dir>` / `-o <filename_or_dir>`**: Defines the name of the output file or directory. Defaults: `README.md` for docs, `tests/` for tests, `Dockerfile` for Docker, `.github/workflows/ci.yml` for GitHub Actions.
*   **`--client <openai|gemini>` / `-c <openai|gemini>`**: Choose the AI client to use for generation. Options are `openai` or `gemini` (default: `gemini`). Case-insensitive.
*   **`--key <your-api-key>` / `-k <your-api-key>`**: Provide your API key directly. This will take precedence over environment variables.
*   **`--test` / `-t`**: Generate `pytest` test files instead of a README.
*   **`--docker`**: Generate a `Dockerfile` for the project.
*   **`--gha`**: Generate a GitHub Actions (CI/CD) workflow.
*   **`--init <project_name>`**: Bootstrap a new Python project with the given project name, creating a basic scaffold.
*   **`--ignore-dirs <dir1> <dir2>...`**: A space-separated list of directory names to ignore during scanning (e.g., `.git __pycache__ node_modules`).
*   **`--ignore-exts <ext1> <ext2>...`**: A space-separated list of file extensions to ignore (e.g., `.tmp .pyc .log`).

**Examples:**

1.  To document a project located at `/path/to/my-other-project` and save the output to `PROJECT_DOCS.md` using the default Gemini model:

    ```bash
    docify --path /path/to/my-other-project --output PROJECT_DOCS.md
    ```

2.  To use the OpenAI client for README generation:

    ```bash
    docify --client openai
    ```

3.  To use the OpenAI client and provide the API key directly (overriding any environment variable):

    ```bash
    docify --client openai --key sk-YOUR_OPENAI_API_KEY
    ```

4.  To generate `pytest` tests for the current project using the Gemini client, ignoring `dist` and `build` directories:

    ```bash
    docify --test --client gemini --ignore-dirs dist build
    ```

5.  To generate a `Dockerfile` for the current project:

    ```bash
    docify --docker
    ```

6.  To generate a GitHub Actions workflow for the current project:

    ```bash
    docify --gha
    ```

7.  To initialize a new Python project named `my_new_app`:

    ```bash
    docify --init my_new_app
    ```