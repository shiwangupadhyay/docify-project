import os
import argparse
import json
import re

from .dataset_extractor import extract_schema_and_sample
from .scanner import get_project_context, get_project_structure
from .generator import Generator


def main():
    """
    The main function to run the command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="AI-Powered Project Documentation Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # --- General Configuration Arguments ---
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
        help='The name of the output file/folder. Defaults: README.md, tests/, etc.'
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

    # --- Mutually Exclusive Action Group ---
    # Ensures only one of these primary actions can be run at a time.
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        '-t', '--test',
        action='store_true',
        help='Generate pytest test files.'
    )
    action_group.add_argument(
        '--docker',
        action='store_true',
        help='Generate a Dockerfile for this project.'
    )
    action_group.add_argument(
        '--gha',
        action='store_true',
        help='Generate a GitHub Actions workflow (CI/CD).'
    )
    action_group.add_argument(
        '--init',
        type=str,
        help='Bootstrap a new Python project with the given project name.'
    )
    action_group.add_argument(
        '--docstring',
        type=str,
        help='Add docstrings to a given Python file (relative path).'
    )
    action_group.add_argument(
        '--notebook',
        action='store_true',
        help='Generate a starter Jupyter Notebook with analysis pipelines/tests.'
    )
    action_group.add_argument(
        '--model-card',
        action='store_true',
        help='Generate a Model Card (MODEL_CARD.md) for ML/AI projects.'
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

    # --- Scanning project context (for all remaining actions) ---
    print(f"Scanning project directory: {os.path.abspath(args.path)}")

    if args.notebook:
        # Use lightweight structure for big-context tasks
        project_context = get_project_structure(args.path)
    else:
        project_context = get_project_context(
            args.path,
            ignore_dirs=args.ignore_dirs,
            ignore_exts=args.ignore_exts
        )

    if not project_context.strip():
        print("Warning: No readable files found in the specified directory.")
        return


    # --- Dataset and Schema Extraction (only for relevant tasks) ---
    dataset_context = ""
    if args.notebook or args.model_card:
        print("Scanning for datasets...")
        dataset_info = extract_schema_and_sample(
                        args.path, 
                        n=5,
                        ignore_dirs=args.ignore_dirs,
                        ignore_exts=args.ignore_exts
                        )

        if dataset_info:
            dataset_context = json.dumps(dataset_info, indent=2)

    # --- Tests Generation ---
    if args.test:
        print("Mode: Generating pytest tests...")
        if args.client == 'openai':
            tests_json_str = generator.generate_test_openai(project_context)
        else:
            tests_json_str = generator.generate_test_gemini(project_context)

        tests = None
        try:
            cleaned = tests_json_str.strip()
            cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.MULTILINE)
            cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE)
            tests = json.loads(cleaned)

        except json.JSONDecodeError:
            print("Initial JSON parsing failed. Asking the model to correct the syntax...")
            
            if args.client == 'openai':
                fixed_json_str = generator.fix_json_openai(tests_json_str)
            else:
                fixed_json_str = generator.fix_json_gemini(tests_json_str)
            
            try:
                cleaned = fixed_json_str.strip()
                cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.MULTILINE)
                cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE)
                tests = json.loads(cleaned)
                print("Successfully parsed the corrected JSON.")
            except json.JSONDecodeError as final_e:
                print(f"Error: The model could not fix the JSON. Parsing failed again: {final_e}")
                print("\n--- Raw output from model (for debugging) ---\n")
                print(tests_json_str)
                return

        if tests:
            try:
                for filepath, content in tests.items():
                    if not isinstance(content, str):
                        print(f"Warning: Content for '{filepath}' is not a string, skipping.")
                        continue

                    out_path = os.path.join(args.output or ".", filepath)
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(content)
                print("Successfully generated test files.")
            except Exception as e:
                print(f"Error writing test files to disk: {e}")
        return

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

# --- Github action workflow config YAML Generation ---
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

    # --- Startup Notebook Generation ---
    elif args.notebook:
        print("Mode: Generating Jupyter Notebook...")
        
        if args.client == 'openai':
            nb_content = generator.generate_notebook_openai(project_context, dataset_context)
        else:
            nb_content = generator.generate_notebook_gemini(project_context, dataset_context)

        # Remove top/bottom ``` if present
        if nb_content.startswith("```"):
            nb_content = "\n".join(nb_content.splitlines()[1:])
        if nb_content.endswith("```"):
            nb_content = "\n".join(nb_content.splitlines()[:-1])

        output_file = args.output or "notebook.ipynb"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(nb_content)
            print(f"Successfully generated Jupyter Notebook at {output_file}")
        except Exception as e:
            print(f"Error saving notebook: {e}")


# --- Model Card Generation ---
    elif args.model_card:
        print("Mode: Generating Model Card...")

        if args.client == 'openai':
            mc_content = generator.generate_model_card_openai(project_context, dataset_context)
        else:
            mc_content = generator.generate_model_card_gemini(project_context, dataset_context)

        # Remove top/bottom ``` if present
        if mc_content.startswith("```"):
            mc_content = "\n".join(mc_content.splitlines()[1:])
        if mc_content.endswith("```"):
            mc_content = "\n".join(mc_content.splitlines()[:-1])

        output_file = args.output or "MODEL_CARD.md"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(mc_content)
            print(f"Successfully generated Model Card at {output_file}")
        except Exception as e:
            print(f"Error saving Model Card: {e}")




# --- Default Action: README/Docs Generation ---
    else:
        print("Mode: Generating README/docs...")
        if args.client == 'openai':
            readme_content = generator.generate_readme_openai(project_context)
        else:
            readme_content = generator.generate_readme_gemini(project_context)

        output_file = args.output or "README.md"
        try:
            cleaned_content = readme_content.strip()

            if cleaned_content.startswith("```"):
                first_line_end = cleaned_content.find("\n")
                if first_line_end != -1:
                    cleaned_content = cleaned_content[first_line_end:].strip()

            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3].strip()

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Successfully generated and saved to {output_file}")
        except Exception as e:
            print(f"Error saving README/docs: {e}")



if __name__ == "__main__":
    main()