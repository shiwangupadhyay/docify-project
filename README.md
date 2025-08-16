# Docify AI 🚀

**Instantly generate beautiful, comprehensive `README.md` files for your local projects using the power of AI.**

## What is Docify?

Every great project needs great documentation, but writing it is often a tedious, manual process. Docify is a command-line tool that automates this entire workflow. It intelligently scans your project's file structure and source code, understands what your project does, and uses a powerful language model to generate a high-quality `README.md` file in seconds.

Stop writing docs and start shipping code.

## Key Features ✨

* **🤖 AI-Powered Content Generation**: Leverages large language models to write human-like, technical documentation.

* **📂 Intelligent Code Analysis**: Scans your entire project directory to understand its purpose, technologies, and structure.

* **⚙️ Simple Command-Line Interface**: Generate a complete README with a single command: `docify`.

* **🚀 Fast and Efficient**: Go from a messy project folder to a polished README in under a minute.

* **🔧 Customizable**: Easily specify the project path and output file name.

## Installation

Docify is published on PyPI and can be installed on any machine with Python 3.8+ using pip.

pip install docify-ai

## Usage

Using Docify is incredibly simple.

### 1. Set Your API Key

First, you need to make your **Google Gemini API key** available as an environment variable. This is a one-time setup per machine. You can get a key from the [Google AI Studio](https://aistudio.google.com/app/apikey) for free.

**macOS / Linux:**

export GEMINI_API_KEY='your-secret-api-key'
*(To make this permanent, add the line to your `~/.zshrc` or `~/.bashrc` file.)*

**Windows:**

$Env:GEMINI_API_KEY="your-secret-api-key"
### 2. Run Docify

Navigate to any project directory you want to document and run the command:

docify
That's it! The tool will scan the current directory and create a `README.md` file with the AI-generated content.

### Command-Line Options

You can also specify the path to your project and the desired output file.

* **`--path`**: The root directory of the project to document. Defaults to the current directory (`.`).

* **`--output`**: The name of the output file. Defaults to `README.md`.

**Example:**

docify --path /path/to/my-other-project --output DOCS.md
## How It Works

Docify is built with a clean, modular architecture:

1. **Scanner (`scanner.py`)**: Traverses the specified project directory, ignoring unnecessary files (like `.git`, `venv`), and aggregates all source code into a single context string.

2. **Generator (`generator.py`)**: Takes the context string and feeds it to the **Google Gemini API** via LangChain, using a carefully crafted prompt to generate the Markdown content.

3. **CLI (`cli.py`)**: Provides the user-friendly command-line interface using `argparse`, orchestrating the scanner and generator to deliver the final `README.md` file.

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please open an issue or submit a pull request on our [GitHub repository](https://github.com/your-username/docify-project).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.