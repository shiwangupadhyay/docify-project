# Docify AI 🚀: Intelligent Documentation for Your Code

A versatile AI-powered command-line tool for instantly generating comprehensive `README.md` files, pytest tests, and Mermaid workflow diagrams for your local projects, powered by Google Gemini and OpenAI GPT models.


## Key Features ✨

*   **🤖 AI-Powered Content Generation**: Leverages large language models (Google Gemini and OpenAI GPT) to write human-like, technical documentation.
*   **💡 Multi-Format Output**: Generate `README.md` files, receive runnable pytest tests, or visualize project workflows with Mermaid diagrams.
*   **📂 Intelligent Code Analysis**: Scans your entire project directory, intelligently ignoring irrelevant files and directories, to understand its purpose, technologies, and structure.
*   **⚙️ Flexible AI Client Selection**: Choose between Google Gemini and OpenAI GPT models for content generation directly from the command line.
*   **🔑 API Key Management**: Supports API keys via environment variables or direct command-line arguments for both Gemini and OpenAI.
*   **🚀 Fast and Efficient**: Go from a messy project folder to a polished README, tests, or workflows in under a minute.
*   **🔧 Customizable Output**: Easily specify the project path to analyze and the desired output file or directory name.


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

*   **`--path <directory>` / `-p <directory>`**: Specifies the root directory of the project to be documented. Defaults to the current working directory (`.`).
*   **`--output <filename>` / `-o <filename>`**: Defines the name of the output file/folder. Defaults: `README.md` for docs, `tests/` for tests, `WORKFLOWS.md` for workflows.
*   **`--client <openai|gemini>` / `-c <openai|gemini>`**: Choose the AI client to use for generation. Options are `openai` or `gemini` (default: `gemini`). Case-insensitive.
*   **`--key <your-api-key>` / `-k <your-api-key>`**: Provide your API key directly. This will take precedence over environment variables.
*   **`--test` / `-t`**: Generate `pytest` test files instead of a README.
*   **`--workflow` / `-w`**: Generate Mermaid workflow diagrams instead of a README.

**Examples:**

1.  To document a project located at `/path/to/my-other-project` and save the output to `DOCS.md` using the default Gemini model:

    ```bash
    docify --path /path/to/my-other-project --output DOCS.md
    ```

2.  To use the OpenAI client for README generation:

    ```bash
    docify --client openai
    ```

3.  To use the OpenAI client and provide the API key directly (overriding any environment variable):

    ```bash
    docify --client openai --key sk-YOUR_OPENAI_API_KEY
    ```

4.  To generate `pytest` tests for the current project using the Gemini client:

    ```bash
    docify --test --client gemini
    ```

5.  To generate Mermaid workflow diagrams and save them to `project-workflows.md`:

    ```bash
    docify --workflow --output project-workflows.md
    ```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog 📜

See the [CHANGELOG.md](CHANGELOG.md) file for a history of changes and release notes.