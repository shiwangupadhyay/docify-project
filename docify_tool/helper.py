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