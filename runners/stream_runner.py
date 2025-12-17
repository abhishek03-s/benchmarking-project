# runners/stream_runner.py

import psutil
from utils.shell import run_command
from utils.auto_params.engine import get_auto_params

def _get_sysinfo():
    return {
        "cpu": {
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
        },
        "memory": {
            "total": psutil.virtual_memory().total,
        },
    }

def run_stream():
    """
    Run STREAM on a single node.
    Uses OMP_NUM_THREADS = number of physical cores by default.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("stream", sysinfo)

    threads = params.get("threads", sysinfo["cpu"]["cores"])

    env = {
        "OMP_NUM_THREADS": str(threads),
    }

    cmd = "stream"

    rc, out, err = run_command(cmd, env=env)

    return {
        "tool": "stream",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
