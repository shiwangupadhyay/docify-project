# Docify AI 🚀

**Instantly generate beautiful, comprehensive `README.md` files for your local projects using the power of AI.**

## Table of Contents

*   [What is Docify?](#what-is-docify)
*   [Key Features ✨](#key-features-%E2%9C%A8)
*   [Project Structure 📂](#project-structure-%F0%9F%93%82)
*   [Technologies Used 🛠️](#technologies-used-%F0%9F%9B%A0%EF%B8%8F)
*   [Installation 📦](#installation-%F0%9F%93%A6)
*   [Usage 🚀](#usage-%F0%9F%9A%80)
    *   [1. Set Your API Key](#1-set-your-api-key)
    *   [2. Run Docify](#2-run-docify)
    *   [Command-Line Options](#command-line-options)
*   [How It Works 🧠](#how-it-works-%F0%9F%A7%A0)
*   [Contributing 🤝](#contributing-%F0%9F%A4%9D)
*   [License 📄](#license-%F0%9F%93%84)

## What is Docify?

Every great project needs great documentation, but writing it is often a tedious, manual process. Docify is a command-line tool that automates this entire workflow. It intelligently scans your project's file structure and source code, understands what your project does, and uses a powerful language model to generate a high-quality `README.md` file in seconds.

Stop writing docs and start shipping code.

## Key Features ✨

*   **🤖 AI-Powered Content Generation**: Leverages large language models (specifically Google Gemini) to write human-like, technical documentation.
*   **📂 Intelligent Code Analysis**: Scans your entire project directory, intelligently ignoring irrelevant files and directories, to understand its purpose, technologies, and structure.
*   **⚙️ Simple Command-Line Interface**: Generate a complete README with a single, intuitive command: `docify`.
*   **🚀 Fast and Efficient**: Go from a messy project folder to a polished README in under a minute.
*   **🔧 Customizable**: Easily specify the project path to analyze and the desired output file name.

## Project Structure 📂

The project is structured to be modular and easy to navigate:

```
.
├── LICENSE
├── README.md
├── pyproject.toml
└── docify_tool/
    ├── __init__.py
    ├── cli.py
    ├── generator.py
    └── scanner.py
```

*   `LICENSE`: Contains the MIT License details for the project.
*   `README.md`: This very file, providing an overview and instructions.
*   `pyproject.toml`: Project metadata, dependencies, and build configuration.
*   `docify_tool/`: The core source code for the Docify CLI.
    *   `__init__.py`: Marks the directory as a Python package.
    *   `cli.py`: Handles command-line argument parsing and orchestrates the scanning and generation process.
    *   `generator.py`: Interfaces with the AI model (Google Gemini) to generate README content.
    *   `scanner.py`: Traverses the project directory, collects file content, and builds the project context.

## Technologies Used 🛠️

*   **Python**: The core programming language for the application (Python 3.8+).
*   **LangChain**: Framework for developing applications powered by language models.
    *   `langchain-openai` (used for `langchain_google_genai` integration)
    *   `langchain-core`
*   **Google Gemini API**: The underlying large language model used for content generation.
*   **Setuptools**: Used for packaging and distribution of the Python project.
*   **Argparse**: Python's standard library for parsing command-line arguments.

## Installation 📦

Docify is published on PyPI and can be installed on any machine with Python 3.8+ using `pip`.

```bash
pip install docify-ai
```

## Usage 🚀

Using Docify is incredibly simple.

### 1. Set Your API Key

First, you need to make your **Google Gemini API key** available as an environment variable. This is a one-time setup per machine. You can get a key from the [Google AI Studio](https://aistudio.google.com/app/apikey) for free.

**macOS / Linux:**

```bash
export GEMINI_API_KEY='your-secret-api-key'
```
*(To make this permanent, add the line to your `~/.zshrc` or `~/.bashrc` file.)*

**Windows (PowerShell):**

```powershell
$Env:GEMINI_API_KEY="your-secret-api-key"
```

### 2. Run Docify

Navigate to any project directory you want to document and run the command:

```bash
docify
```
That's it! The tool will scan the current directory and create a `README.md` file with the AI-generated content.

### Command-Line Options

You can also specify the path to your project and the desired output file using the following options:

*   **`--path`**: The root directory of the project to document. Defaults to the current directory (`.`).
*   **`--output`**: The name of the output file. Defaults to `README.md`.

**Example:**

```bash
docify --path /path/to/my-other-project --output DOCS.md
```

## How It Works 🧠

Docify is built with a clean, modular architecture:

1.  **Scanner (`scanner.py`)**: Traverses the specified project directory, ignoring unnecessary files (like `.git`, `venv`, `node_modules`, `__pycache__`), and aggregates all relevant source code into a single context string.
2.  **Generator (`generator.py`)**: Takes the aggregated project context string and feeds it to the **Google Gemini API** via LangChain, using a carefully crafted prompt to generate the Markdown content for the README.
3.  **CLI (`cli.py`)**: Provides the user-friendly command-line interface using `argparse`, orchestrating the scanner and generator to deliver the final `README.md` file.

## Contributing 🤝

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please open an issue or submit a pull request on our [GitHub repository](https://github.com/your-username/docify-project) (replace with actual link).

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.