import os
import argparse
from .scanner import get_project_context
from .generator import generate_readme

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
    
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set. set it using $Env:GEMINI_API_KEY=<your-secret-api-key> command in your terminal")
        return

    print(f"🔍 Scanning project directory: {os.path.abspath(args.path)}")
    
    project_context = get_project_context(args.path)
    
    if not project_context.strip():
        print("⚠️ Warning: No readable files found in the specified directory.")
        return
        
    readme_content = generate_readme(project_context, api_key)
    
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ Successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    main()