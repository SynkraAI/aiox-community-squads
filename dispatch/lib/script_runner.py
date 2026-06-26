"""
Dispatch Squad — Script Runner
Shared subprocess utility for orchestrator scripts.

Resolves script paths, executes via subprocess, parses JSON output.
All dispatch scripts should use this instead of calling subprocess directly.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def run_script(
    script_name: str,
    args: Optional[List[str]] = None,
    timeout: int = 120,
    project_root: str = ".",
    stdin_data: Optional[str] = None,
) -> Dict[str, Any]:
    """Run a dispatch script and parse its JSON output.

    Args:
        script_name: Script filename (e.g., "cost-tracker.py", "validate-dispatch-gate.sh")
        args: CLI arguments to pass after the script name
        timeout: Max execution time in seconds
        project_root: Project root for path resolution
        stdin_data: Optional string to pipe to stdin

    Returns:
        {"ok": True, "data": {...}} on success (stdout parsed as JSON)
        {"ok": False, "error": "...", "exit_code": N, "stderr": "..."} on failure
    """
    root = Path(project_root)
    script_path = root / "squads" / "dispatch" / "scripts" / script_name

    if not script_path.exists():
        return {"ok": False, "error": f"Script not found: {script_path}", "exit_code": -1, "stderr": ""}

    # Build command based on file extension
    if script_name.endswith(".sh"):
        cmd = ["bash", str(script_path)]
    elif script_name.endswith(".py"):
        cmd = [sys.executable, str(script_path)]
    else:
        cmd = [str(script_path)]

    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(root),
            stdin=subprocess.PIPE if stdin_data else None,
            input=stdin_data,
        )

        if result.returncode != 0:
            return {
                "ok": False,
                "error": result.stderr.strip() or f"Exit code {result.returncode}",
                "exit_code": result.returncode,
                "stderr": result.stderr.strip(),
                "stdout": result.stdout.strip(),
            }

        # Try to parse stdout as JSON
        stdout = result.stdout.strip()
        if stdout:
            try:
                data = json.loads(stdout)
                return {"ok": True, "data": data}
            except json.JSONDecodeError:
                # Script succeeded but output is not JSON — return raw
                return {"ok": True, "data": {"raw_output": stdout}}
        else:
            return {"ok": True, "data": {}}

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": f"Script timed out after {timeout}s",
            "exit_code": -2,
            "stderr": "TimeoutExpired",
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "exit_code": -3,
            "stderr": str(e),
        }
