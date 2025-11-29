# backend/utils.py
import re

def extract_json_substring(text: str) -> str:
    """
    Try to extract a JSON substring from a model output.
    Returns a string that can be passed to json.loads.
    """
    # Find the first { and last } to attempt to isolate JSON
    try:
        start = text.index("{")
        end = text.rindex("}")
        candidate = text[start:end+1]
        # Basic cleanup: remove leading/trailing backticks or markdown fences
        candidate = candidate.strip().strip("`")
        # Replace problematic single quotes with double quotes if it's simple dict-like
        # But prefer not to aggressively change to avoid corrupting valid JSON.
        return candidate
    except ValueError:
        # fallback: return whole text
        return text

