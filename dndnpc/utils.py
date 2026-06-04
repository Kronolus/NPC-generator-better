import json

def safe_json_list(raw):
    try:
        value = json.loads(raw or "[]")
        return value if isinstance(value, list) else []
    except Exception:
        return []

def safe_json_dict(raw):
    try:
        value = json.loads(raw or "{}")
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}

def to_json(value):
    return json.dumps(value, ensure_ascii=False)

def short(text, length=90):
    if not text:
        return ""
    value = str(text).replace("\n", " ")
    return value if len(value) <= length else value[:length - 1] + "…"
