# utils/shell.py

import subprocess
from typing import Tuple, Optional, Dict

def run_command(
    cmd: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
) -> Tuple[int, str, str]:
    """
    Run a shell command and capture return code, stdout, stderr.
    Does not raise on error; caller decides based on return code.
    """
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr
