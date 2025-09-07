import os
import csv
import json

DATA_EXTS = [".csv", ".tsv", ".json", ".ndjson", ".parquet", ".xlsx", ".xls"]
MAX_FIELD_LEN = 100  # max chars per field in sample
MAX_LIST_ITEMS = 5   # max items in nested lists for JSON
MAX_SAMPLE_ROWS = 3  # rows to show per dataset

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

def extract_csv_tsv(file_path, sep=",", n=MAX_SAMPLE_ROWS):
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

def extract_json(file_path, n=MAX_SAMPLE_ROWS):
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

def summarize_datasets(dataset_info):
    """
    Convert dataset info to a compact, LLM-friendly text summary.
    """
    lines = []
    for file, info in dataset_info.items():
        lines.append(f"File: {file}")

        schema = info.get("schema", {})
        if isinstance(schema, dict):
            schema_str = ", ".join(f"{k} ({v})" for k, v in schema.items())
            lines.append(f"Columns: {schema_str}")
        else:
            lines.append(f"Columns: {schema}")

        sample_rows = info.get("sample", [])
        if sample_rows:
            lines.append("Sample rows:")
            for row in sample_rows:
                if isinstance(row, dict):
                    row_values = [str(v)[:MAX_FIELD_LEN] for v in row.values()]
                    lines.append(" | ".join(row_values))
                elif isinstance(row, list):
                    row_values = [str(v)[:MAX_FIELD_LEN] for v in row]
                    lines.append(" | ".join(row_values))
            if len(sample_rows) >= MAX_SAMPLE_ROWS:
                lines.append(f"... more rows available")
        lines.append("")  # blank line between files
    return "\n".join(lines)

def extract_and_summarize(project_path, ignore_dirs=None):
    """
    Main function: walks project path, extracts supported datasets,
    and returns compact text summary.
    """
    ignore_dirs = set(ignore_dirs or [])
    dataset_info = {}

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in DATA_EXTS:
                continue

            file_path = os.path.join(root, file)
            if ext == ".csv":
                dataset_info[file] = extract_csv_tsv(file_path)
            elif ext == ".tsv":
                dataset_info[file] = extract_csv_tsv(file_path, sep="\t")
            elif ext in [".json", ".ndjson"]:
                dataset_info[file] = extract_json(file_path)
            elif ext in [".parquet", ".xlsx", ".xls"]:
                dataset_info[file] = {
                    "path": file_path,
                    "note": "Format detected but requires external library"
                }

    return summarize_datasets(dataset_info)