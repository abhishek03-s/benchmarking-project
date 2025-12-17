# runners/hpl_runner.py

from utils.shell import run_command
from utils.system_info_hpl import detect_hpl_config
from utils.auto_params.engine import get_auto_params

def run_hpl():
    """
    Run HPL in single-node mode.
    """
    sysinfo_raw = detect_hpl_config()
    sysinfo = {
        "cpu": {
            "cores": sysinfo_raw["cores"],
            "sockets": sysinfo_raw["P"],
        },
        "memory": {"total": sysinfo_raw["memory"]},
    }

    params = get_auto_params("hpl", sysinfo)

    ranks = sysinfo["cpu"]["cores"]

    cmd = f"mpirun -np {ranks} xhpl"

    rc, out, err = run_command(cmd)

    return {
        "tool": "hpl",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo_raw,
    }
