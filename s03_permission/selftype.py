
from pathlib import Path

WORKDIR = Path.cwd()



DENY_LIST = [
    "rm -rf", "rm -rf", "sudo", "chmod", "chown", "dd", "mkfs", "mount", "umount",
]
def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

def run_bash(cmd:str) -> str:
    try:
        r = subprocess.run(cmd, shell = True, cwd = WORKDIR,
                           capture_output = True, text = True, timeout = 120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def run_read(path: str, limit: int) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limt < len(lines):
            lines = lines[:lines] + [f"... ({len(lines) - limit} more lines)"]
            return "\n".join(lines)
    except Exception as e:
        return f"Error reading file: {e}"

def run_write(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error writing file: {e}"
    
def run_glob(pattern: str) -> str:
    import glob as g
    try:
        results = []
        for match in g.glob(pattern, root_dir=WORKDIR):
            if (WORKDIR / match).resolve().is_relative_to(WORKDIR):
                results.append(match)
        return "\n".join(results) if results else "(no matches)"
    except Exception as e:
        return f"Error: {e}"

TOOLS = [
    {'name': 'run_bash', 
     'description':'Run a bash command in the workspace. Returns the output or error message. Deny list: ' + ', '.join(DENY_LIST),
     input_schema = {
         'type': 'object',
         properties: {
             'command': {'type': 'string', 'description': 'The bash command to run.'}
         }
     }}
]