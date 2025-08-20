import google.generativeai as genai
from openai import OpenAI

def generate_readme_gemini(project_context, api_key):
    """
    Generates a README.md file content using the Google Gemini model.
    """
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""You are an expert technical writer specializing in creating beautiful, clear, and comprehensive README.md files.
Based on the following complete project context, which includes file paths and their contents, generate an attractive and dynamic README.md file in markdown format, and give clean code only not anything else.

The README should include:
1. An engaging project title.
2. A concise one-liner description.
3. A 'Project Structure' showing structure of project.
4. A 'Key Features' section using bullet points.
5. A 'Technologies Used' section.
6. Clear 'Installation' and 'Usage' instructions based on the files (e.g., requirements.txt, package.json).
7. If it's a web service, document the API endpoints you find otherwise don't add this section.

Here is the project context:
{project_context}
markdown :"""

    print("🤖 Docify-AI is analyzing the project and writing the DOCS...")
    
    response = model.generate_content(prompt)
    
    return response.text


def generate_readme_openai(project_context, api_key):
    """
    Generates a README.md file content using the OpenAI API (GPT model).
    """
    client = OpenAI(api_key=api_key)

    system_prompt = """You are an expert technical writer specializing in creating beautiful, clear, and comprehensive README.md files.
Based on the provided project context, generate an attractive and dynamic README.md file in markdown format.
Your output should be only the clean markdown code and nothing else."""

    user_prompt = f"""Please generate the README.md file based on the following instructions and project context.

The README should include:
1. An engaging project title.
2. A concise one-liner description.
3. A 'Project Structure' showing the structure of the project.
4. A 'Key Features' section using bullet points.
5. A 'Technologies Used' section.
6. Clear 'Installation' and 'Usage' instructions based on the files (e.g., requirements.txt, package.json).
7. If it's a web service, document the API endpoints you find; otherwise, do not add this section.

Here is the complete project context:
{project_context}
"""
    print("🤖 Docify-AI is analyzing the project and writing the DOCS...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content