# runners/imb_runner.py

from utils.shell import run_command
from utils.auto_params.engine import get_auto_params
import psutil

def _get_sysinfo():
    return {"cpu": {"cores": psutil.cpu_count(logical=False)}}

def run_imb():
    """
    Run Intel MPI Benchmarks (IMB-MPI1) in single-node mode.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("imb", sysinfo)

    ranks = params["mpi_ranks"]
    iterations = params["iterations"]

    # Example: just PingPong; you can extend to AllPingPong, PingPong + Allreduce, etc.
    cmd = f"mpirun -np {ranks} IMB-MPI1 PingPong -iter {iterations}"

    rc, out, err = run_command(cmd)

    return {
        "tool": "imb",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
