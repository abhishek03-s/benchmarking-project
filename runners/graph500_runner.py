# runners/graph500_runner.py

from utils.shell import run_command
from utils.auto_params.engine import get_auto_params
import psutil

def _get_sysinfo():
    return {"cpu": {"cores": psutil.cpu_count(logical=False)}}

def run_graph500():
    """
    Run Graph500 in single-node mode.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("graph500", sysinfo)

    scale = params["scale"]
    edge_factor = params["edge_factor"]
    ranks = sysinfo["cpu"]["cores"]

    cmd = f"mpirun -np {ranks} graph500_mpi_simple -s {scale} -e {edge_factor}"

    rc, out, err = run_command(cmd)

    return {
        "tool": "graph500",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
