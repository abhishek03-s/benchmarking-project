# runners/ior_runner.py

import psutil
from utils.shell import run_command
from utils.auto_params.engine import get_auto_params

def _get_sysinfo():
    return {
        "cpu": {"cores": psutil.cpu_count(logical=False)},
        "memory": {"total": psutil.virtual_memory().total},
    }

def run_ior(target_dir: str = "/tmp"):
    """
    Run IOR in single-node mode, using mpirun over local ranks.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("ior", sysinfo)

    transfer = params["transfer_size"]
    block = params["block_size"]
    file_size_bytes = params["file_size"]  # not used directly in cmd here
    ranks = params["mpi_ranks"]

    cmd = (
        f"mpirun -np {ranks} ior "
        f"-t {transfer} -b {block} "
        f"-o {target_dir}/ior_test_file "
        f"-F -w -r -k"
    )

    rc, out, err = run_command(cmd)

    return {
        "tool": "ior",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
        "target_dir": target_dir,
    }
