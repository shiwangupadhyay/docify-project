import os
import argparse
import json
import re
from .scanner import get_project_context
from .generator import Generator


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
        help='The name of the output file/folder. Defaults: README.md, tests/, Dockerfile, or .github/workflows/ci.yml.'
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
        help='Generate pytest test files.'
    )
    parser.add_argument(
        '--docker',
        action='store_true',
        help='Generate a Dockerfile for this project.'
    )
    parser.add_argument(
        '--gha',
        action='store_true',
        help='Generate a GitHub Actions workflow (CI/CD).'
    )
    parser.add_argument(
        '--init',
        type=str,
        help='Bootstrap a new Python project with the given project name.'
    )
    parser.add_argument(
        '--docstring',
        type=str,
        help='Add docstrings to a given Python file (relative path).'
    )
    parser.add_argument(
        '--ignore-dirs',
        nargs='+',
        default=['.git', '__pycache__', 'node_modules', '.vscode', 'venv', '.venv', 'dist', 'build', '.github'],
        help="A space-separated list of directory names to ignore."
    )
    parser.add_argument(
        '--ignore-exts',
        nargs='+',
        default=['.tmp', '.pyc', '.env', '.log', '.DS_Store', '.lock', '.gitignore'],
        help="A space-separated list of file extensions to ignore."
    )

    args = parser.parse_args()

    # --- API key handling ---
    if args.client == 'gemini':
        api_key = args.key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("""No Gemini API key found.

Either pass it with --key argument or set an environment variable:

Windows (PowerShell):
$Env:GEMINI_API_KEY="your-secret-api-key"

macOS / Linux (bash):
export GEMINI_API_KEY='your-secret-api-key'
""")
            return
    else:
        api_key = args.key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("""No OpenAI API key found.

Either pass it with --key argument or set an environment variable:

Windows (PowerShell):
$Env:OPENAI_API_KEY="your-secret-api-key"

macOS / Linux (bash):
export OPENAI_API_KEY='your-secret-api-key'
""")
            return

    # --- Initialize Generator ---
    generator = Generator(api_key)

    # --- Project Init ---
    if args.init:
        project_name = args.init
        print(f"Bootstrapping new Python project: {project_name}")
        if args.client == 'openai':
            scaffold = generator.generate_project_init_openai(project_name)
        else:
            scaffold = generator.generate_project_init_gemini(project_name)

        for filepath, content in scaffold.items():
            out_path = os.path.join(project_name, filepath)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"Project {project_name} initialized successfully.")
        return

    # --- Docstring Generation ---
    if args.docstring:
        file_path = args.docstring
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        print(f"Adding docstrings to {file_path}...")
        if args.client == 'openai':
            updated_code = generator.generate_docstring_openai(code_content)
        else:
            updated_code = generator.generate_docstring_gemini(code_content)

        try:
            cleaned = updated_code.strip()
            cleaned = re.sub(r"^```(?:python)?", "", cleaned, flags=re.MULTILINE).strip()
            cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE).strip()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Docstrings successfully added to {file_path}")
        except Exception as e:
            print(f"Error saving updated file: {e}")
        return

    # --- Scanning project context ---
    print(f"Scanning project directory: {os.path.abspath(args.path)}")
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
            tests_json = generator.generate_test_openai(project_context)
        else:
            tests_json = generator.generate_test_gemini(project_context)

        try:
            cleaned = tests_json.strip()
            cleaned = re.sub(r"^```(?:json)?", "", cleaned)
            cleaned = re.sub(r"```$", "", cleaned)
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

    # --- Dockerfile Generation ---
    elif args.docker:
        print("Mode: Generating Dockerfile...")
        if args.client == 'openai':
            docker_content = generator.generate_dockerfile_openai(project_context)
        else:
            docker_content = generator.generate_dockerfile_gemini(project_context)

        output_file = args.output or "Dockerfile"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(docker_content)
            print(f"Successfully generated Dockerfile at {output_file}")
        except Exception as e:
            print(f"Error saving Dockerfile: {e}")

    # --- GitHub Actions Workflow Generation ---
    elif args.gha:
        print("Mode: Generating GitHub Actions workflow...")
        if args.client == 'openai':
            gha_content = generator.generate_gha_openai(project_context)
        else:
            gha_content = generator.generate_gha_gemini(project_context)

        output_file = args.output or ".github/workflows/ci.yml"
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(gha_content)
            print(f"Successfully generated GitHub Actions workflow at {output_file}")
        except Exception as e:
            print(f"Error saving GitHub Actions workflow: {e}")

    # --- README/Docs Generation (default) ---
    else:
        print("Mode: Generating README/docs...")
        if args.client == 'openai':
            readme_content = generator.generate_readme_openai(project_context)
        else:
            readme_content = generator.generate_readme_gemini(project_context)

        output_file = args.output or "README.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"Successfully generated and saved to {output_file}")
        except Exception as e:
            print(f"Error saving README/docs: {e}")


if __name__ == "__main__":
    main()