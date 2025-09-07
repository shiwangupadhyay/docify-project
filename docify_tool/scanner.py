import os
import json

def read_notebook_source(file_path):
    """Read Jupyter notebook and return concatenated code + markdown cells."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        code_cells = "\n".join("".join(cell["source"]) 
                               for cell in nb.get("cells", []) 
                               if cell.get("cell_type") == "code")
        markdown_cells = "\n".join("".join(cell["source"]) 
                                   for cell in nb.get("cells", []) 
                                   if cell.get("cell_type") == "markdown")
        return code_cells + "\n" + markdown_cells
    except Exception as e:
        return f"[Error reading notebook: {e}]"

def get_project_context(root_dir, ignore_dirs=None, ignore_exts=None):
    """
    Walks through a directory, gets file structure and content,
    returns a formatted string including notes about ignored files/directories.
    """
    ignore_dirs = set(ignore_dirs or [])
    ignore_exts = set(ignore_exts or [])
    full_context = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Track ignored dirs
        ignored_dirs_in_path = [d for d in dirnames if d in ignore_dirs]
        for d in ignored_dirs_in_path:
            full_context.append(f"--- Ignored directory: {os.path.join(dirpath, d)} ---\n")
        
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_dir)

            # Track ignored files
            if any(filename.endswith(ext) for ext in ignore_exts):
                full_context.append(f"--- Ignored file: {relative_path} ---\n")
                continue

            full_context.append(f"--- File: {relative_path} ---\n")
            try:
                if filename.endswith(".ipynb"):
                    content = read_notebook_source(file_path)
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                full_context.append(content)
            except Exception as e:
                full_context.append(f"[Error reading file: {e}]")
            full_context.append("\n\n")

    return "".join(full_context)

def get_project_structure(path, ignore_dirs=None):
    """
    Returns a textual tree structure of the project directory,
    showing ignored directories but not traversing into them.
    """
    ignore_dirs = set(ignore_dirs or [])
    tree = []

    for root, dirs, files in os.walk(path):
        rel = os.path.relpath(root, path)
        if rel == ".":
            tree.append(f"{os.path.basename(path)}/")
        else:
            tree.append(f"{rel}/")

        # Show files in this directory
        for f in files:
            tree.append(f"  {f}")

        # Handle ignored directories: show them but remove from traversal
        for d in dirs[:]:
            if d in ignore_dirs:
                tree.append(f"  {d}/ (ignored)")
                dirs.remove(d)  # Prevent os.walk from entering it

    return "\n".join(tree)
