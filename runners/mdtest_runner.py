# runners/mdtest_runner.py

import os
import psutil
from utils.shell import run_command

def _get_sysinfo():
    return {"cpu": {"cores": psutil.cpu_count(logical=False)}}

def run_mdtest(target_dir: str = "/tmp"):
    """
    Run mdtest in single-node mode with local MPI ranks.
    """
    sysinfo = _get_sysinfo()
    ranks = sysinfo["cpu"]["cores"]

    test_dir = os.path.join(target_dir, "mdtest_dir")
    os.makedirs(test_dir, exist_ok=True)

    cmd = (
        f"mpirun -np {ranks} mdtest "
        f"-d {test_dir} "
        f"-n 1000 -u -F"
    )

    rc, out, err = run_command(cmd)

    return {
        "tool": "mdtest",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "sysinfo": sysinfo,
        "target_dir": target_dir,
    }
