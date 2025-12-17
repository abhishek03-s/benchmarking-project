# runners/netpipe_runner.py

from utils.shell import run_command
from utils.auto_params.engine import get_auto_params
import psutil

def _get_sysinfo():
    return {"cpu": {"cores": psutil.cpu_count(logical=False)}}

def run_netpipe():
    """
    Run NetPIPE (NPmpi) in single-node mode with 2 ranks.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("netpipe", sysinfo)

    max_msg = params["max_message_size"]

    cmd = f"mpirun -np 2 NPmpi -s 1 -e {max_msg}"

    rc, out, err = run_command(cmd)

    return {
        "tool": "netpipe",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
