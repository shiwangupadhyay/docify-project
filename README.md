# Docify AI 🚀

**Instantly generate beautiful, comprehensive `README.md` files for your local projects using the power of AI.**


## Key Features ✨

*   **🤖 AI-Powered Content Generation**: Leverages large language models (specifically Google Gemini) to write human-like, technical documentation.
*   **📂 Intelligent Code Analysis**: Scans your entire project directory, intelligently ignoring irrelevant files and directories, to understand its purpose, technologies, and structure.
*   **⚙️ Simple Command-Line Interface**: Generate a complete README with a single, intuitive command: `docify`.
*   **🚀 Fast and Efficient**: Go from a messy project folder to a polished README in under a minute.
*   **🔧 Customizable**: Easily specify the project path to analyze and the desired output file name.


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