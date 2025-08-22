import os
import argparse
import json
from .scanner import get_project_context
from .generator import (
    generate_readme_gemini, generate_readme_openai,
    generate_test_gemini, generate_test_openai
)


def main():
    """
    The main function to run the command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="AI-Powered Project Documentation Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='.',
        help='The root directory of the project. Defaults to the current directory.'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='The name of the output file/folder. Defaults: README.md for docs, tests/ for tests.'
    )
    parser.add_argument(
        '--client', '-c',
        type=lambda s: s.lower(),
        choices=['openai', 'gemini'],
        default='gemini',
        help='Choose the client: openai or gemini (default: gemini). Case-insensitive.'
    )
    parser.add_argument(
        '--key', '-k',
        type=str,
        default=None,
        help='API key for your selected client (preferred over environment variable).'
    )
    parser.add_argument(
        '-t', '--test',
        action='store_true',
        help='Generate pytest test files instead of README.'
    )
    parser.add_argument(
        '--ignore-dirs',
        nargs='+',
        default=['.git', '__pycache__', 'node_modules', '.vscode', 'venv', '.venv', 'dist', 'build'],
        help="A space-separated list of directory names to ignore."
    )
    parser.add_argument(
        '--ignore-exts',
        nargs='+',
        default=['.tmp','.pyc', '.env', '.log', '.DS_Store', '.lock', '.gitignore'],
        help="A space-separated list of file extensions to ignore (e.g., pyc log svg)."
    )

    args = parser.parse_args()

    if args.client == 'gemini':
        api_key = args.key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("""No Gemini API key found.

Either pass it with --key argument or set an environment variable:

For Windows (PowerShell):
$Env:GEMINI_API_KEY="your-secret-api-key"

For macOS / Linux (bash):
export GEMINI_API_KEY='your-secret-api-key'
""")
            return
    else:
        api_key = args.key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("""No OpenAI API key found.

Either pass it with --key argument or set an environment variable:

For Windows (PowerShell):
$Env:OPENAI_API_KEY="your-secret-api-key"

For macOS / Linux (bash):
export OPENAI_API_KEY='your-secret-api-key'
""")
            return

    print(f"🔍 Scanning project directory: {os.path.abspath(args.path)}")

    project_context = get_project_context(
        args.path, 
        ignore_dirs=args.ignore_dirs, 
        ignore_exts=args.ignore_exts
    )

    if not project_context.strip():
        print("Warning: No readable files found in the specified directory.")
        return

    # --- Test Generation ---
    if args.test:
        print("Mode: Generating pytest tests...")
        if args.client == 'openai':
            tests_json = generate_test_openai(project_context, api_key)
        else:
            tests_json = generate_test_gemini(project_context, api_key)

        import re

        try:
            cleaned = tests_json.strip()
            cleaned = re.sub(r"^```(?:json)?", "", cleaned)
            cleaned = re.sub(r"```$", "", cleaned)
            cleaned = cleaned.strip()

            tests = json.loads(cleaned)

            for filepath, content in tests.items():
                out_path = os.path.join(args.output or ".", filepath)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)
            print("Successfully generated test files.")
        except Exception as e:
            print("Error writing test files:", e)
            print("\n--- Raw output from model (for debugging) ---\n")
            print(tests_json)

    # --- README/Docs Generation ---
    else:
        print("Mode: Generating README/docs...")
        if args.client == 'openai':
            readme_content = generate_readme_openai(project_context, api_key)
        else:
            readme_content = generate_readme_gemini(project_context, api_key)

        output_file = args.output or "README.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"Successfully generated and saved to {output_file}")
        except Exception as e:
            print(f"Error saving README/docs: {e}")


if __name__ == "__main__":
    main()
