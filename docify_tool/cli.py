import os
import argparse
from .scanner import get_project_context
from .generator import generate_readme_gemini, generate_readme_openai


def main():
    """
    The main function to run the command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="🚀 AI-Powered README.md Generator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='The root directory of the project to document. Defaults to the current directory.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='README.md',
        help='The name of the output file. Defaults to README.md.'
    )
    parser.add_argument(
        '--client',
        type=lambda s: s.lower(),
        choices=['openai', 'gemini'],
        default='gemini',
        help='Choose the client: openai or gemini (default: gemini). Case-insensitive.'
    )
    parser.add_argument(
        '--key',
        type=str,
        default=None,
        help='Put the API key of your selected client (this will be preferred over environment variable).'
    )

    args = parser.parse_args()

    if args.client == 'gemini':
        api_key = args.key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("""⚠️ No Gemini API key found.

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
            print("""⚠️ No OpenAI API key found.

Either pass it with --key argument or set an environment variable:

For Windows (PowerShell):
$Env:OPENAI_API_KEY="your-secret-api-key"

For macOS / Linux (bash):
export OPENAI_API_KEY='your-secret-api-key'
""")
            return

    print(f"🔍 Scanning project directory: {os.path.abspath(args.path)}")

    project_context = get_project_context(args.path)

    if not project_context.strip():
        print("⚠️ Warning: No readable files found in the specified directory.")
        return

    if args.client == 'openai':
        readme_content = generate_readme_openai(project_context, api_key)
    else:
        readme_content = generate_readme_gemini(project_context, api_key)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ Successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")


if __name__ == "__main__":
    main()
