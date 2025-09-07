import os
import csv
import json

DATA_EXTS = [".csv", ".tsv", ".json", ".ndjson", ".parquet", ".xlsx", ".xls"]
MAX_FIELD_LEN = 100  # max chars per field in sample
MAX_LIST_ITEMS = 5   # max items in nested lists for JSON

def truncate_value(val):
    """Truncate strings to MAX_FIELD_LEN, recurse for lists/dicts."""
    if val is None:
        return None
    if isinstance(val, str):
        return val if len(val) <= MAX_FIELD_LEN else val[:MAX_FIELD_LEN] + "..."
    if isinstance(val, list):
        return [truncate_value(v) for v in val[:MAX_LIST_ITEMS]]
    if isinstance(val, dict):
        return {k: truncate_value(v) for k, v in val.items()}
    return val

def guess_type(value):
    """Guess the data type of a value, recursively handling lists and dicts."""
    if value is None or value == "":
        return "null"
    if isinstance(value, dict):
        return {k: guess_type(v) for k, v in value.items()}
    if isinstance(value, list):
        if not value:
            return "list(empty)"
        return [guess_type(value[0])]
    try:
        int(str(value))
        return "int"
    except (ValueError, TypeError):
        pass
    try:
        float(str(value))
        return "float"
    except (ValueError, TypeError):
        pass
    lower = str(value).lower()
    if lower in ["true", "false"]:
        return "bool"
    return "string"

def extract_csv_tsv(file_path, sep=",", n=1):
    dataset = {"path": file_path, "schema": {}, "sample": []}
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f, delimiter=sep)
            rows = []
            for i, row in enumerate(reader):
                if i < n:
                    rows.append({k: truncate_value(v) for k, v in row.items()})
                else:
                    break
            dataset["sample"] = rows

            # infer schema
            if rows and reader.fieldnames:
                schema = {}
                for col in reader.fieldnames:
                    values = [row[col] for row in rows if row.get(col) not in (None, "")]
                    schema[col] = guess_type(values[0]) if values else "unknown"
                dataset["schema"] = schema
    except Exception as e:
        return {"path": file_path, "error": str(e)}
    return dataset

def extract_json(file_path, n=1):
    dataset = {"path": file_path, "schema": {}, "sample": []}
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            try:
                content = f.read()
                data = json.loads(content)
                if isinstance(data, list):
                    rows = [truncate_value(d) for d in data[:n]]
                elif isinstance(data, dict):
                    rows = [truncate_value(data)]
            except json.JSONDecodeError:
                f.seek(0)
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                        rows.append(truncate_value(obj))
                    except json.JSONDecodeError:
                        continue
                    if len(rows) >= n:
                        break

        dataset["sample"] = rows
        if rows:
            dataset["schema"] = guess_type(rows[0])
    except Exception as e:
        return {"path": file_path, "error": str(e)}
    return dataset

def extract_schema_and_sample(project_path, n=1, ignore_dirs=None, ignore_exts=None):
    """Walks a directory and extracts info from supported dataset files."""
    ignore_dirs = set(ignore_dirs or [])
    ignore_exts = set(ignore_exts or [])
    
    dataset_info = {}
    for root, dirs, files in os.walk(project_path):
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in DATA_EXTS or file in ignore_exts:
                continue

            file_path = os.path.join(root, file)

            if ext == ".csv":
                dataset_info[file] = extract_csv_tsv(file_path, sep=",", n=n)
            elif ext == ".tsv":
                dataset_info[file] = extract_csv_tsv(file_path, sep="\t", n=n)
            elif ext in [".json", ".ndjson"]:
                dataset_info[file] = extract_json(file_path, n=n)
            elif ext in [".parquet", ".xlsx", ".xls"]:
                dataset_info[file] = {"path": file_path, "note": "Format detected but requires external library"}
    return dataset_info

