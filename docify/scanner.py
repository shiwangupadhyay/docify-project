import os

def get_project_context(root_dir, ignore_dirs=None, ignore_exts=None):
    """
    Walks through a directory, gets the file structure and content,
    and returns it as a single formatted string.
    """
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', 'node_modules', '.vscode', 'venv', 'dist', 'build'}
    if ignore_exts is None:
        ignore_exts = {'.pyc', '.env', '.log', '.DS_Store', '.lock'}

    full_context = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            if any(filename.endswith(ext) for ext in ignore_exts):
                continue

            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_dir)

            full_context.append(f"--- File: {relative_path} ---\n")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    full_context.append(content)
            except Exception as e:
                full_context.append(f"[Error reading file: {e}]")
            full_context.append("\n\n")

    return "".join(full_context)