import json
import re

def _parse_project_init_response(raw_text):
    """
    Parse AI response for project init into a dict {filepath: content}.
    """
    try:
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?", "", cleaned)
        cleaned = re.sub(r"```$", "", cleaned)
        cleaned = cleaned.strip()
        return json.loads(cleaned)
    except Exception as e:
        print("⚠️ Error parsing AI project scaffold response:", e)
        print("Raw output:\n", raw_text)
        return {}
    

import re

def clean_fenced_content(content: str) -> str:
    """
    Safely removes top-level leading/trailing fenced code blocks like
    ```python, ```json, ```yaml, ```docker, ```markdown, ''' etc.
    Leaves nested fences intact.
    """
    if not content:
        return ""

    lines = content.splitlines()

    # Remove first line if it is a fence with optional language
    if lines and re.match(r"^(```|''')\s*\w*\s*$", lines[0], re.IGNORECASE):
        lines = lines[1:]

    # Remove last line if it is a fence
    if lines and re.match(r"^(```|''')\s*$", lines[-1]):
        lines = lines[:-1]

    return "\n".join(lines).strip()

