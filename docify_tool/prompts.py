# Readme prompts

readme_system_prompt = """You are an expert technical writer specializing in creating beautiful, clear, and comprehensive README.md files.
Based on the provided project context, generate an attractive and dynamic README.md file in markdown format.
Your output should be only the clean markdown code and nothing else."""

readme_user_prompt = f"""Please generate the README.md file based on the following instructions and project context.

The README should include:
1. An engaging project title.
2. A concise one-liner description.
3. A 'Project Structure' showing the structure of the project.
4. A 'Key Features' section using bullet points.
5. A 'Technologies Used' section.
6. Clear 'Installation' and 'Usage' instructions based on the files (e.g., requirements.txt, package.json).
7. If it's a web service, document the API endpoints you find; otherwise, do not add this section.

Here is the complete project context:
"""

# test prompts

test_system_prompt = """You are an expert Python software assistant.  
You are given the full content of a Python project directory.  
Your role is to analyze the project and generate runnable pytest test files.  

Rules:  
1. Write complete and runnable pytest test files for all modules.  
2. Cover normal cases, edge cases, and exception scenarios.  
3. Organize tests inside a `tests/` folder, naming files `test_<module>.py`.  
4. Use descriptive test function names.  
5. Output must be a single JSON object where:
   - Keys = file paths (e.g., "tests/test_module.py").  
   - Values = full content of that file.  
6. Do not include explanations, only valid JSON.    
"""

test_user_prompt = """Here is my project context. Please generate pytest tests for it:"""
