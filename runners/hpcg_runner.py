# runners/hpcg_runner.py

import psutil
from utils.shell import run_command
from utils.auto_params.engine import get_auto_params

def run_hpcg():
    """
    Run HPCG in single-node mode.
    Assumes HPCG input file is already present/auto-generated.
    """
    cores = psutil.cpu_count(logical=False)
    sysinfo = {"cpu": {"cores": cores}}

    params = get_auto_params("hpcg", sysinfo)

    cmd = f"mpirun -np {cores} xhpcg"

    rc, out, err = run_command(cmd)

    return {
        "tool": "hpcg",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
