# runners/osu_runner.py

from utils.shell import run_command
from utils.auto_params.engine import get_auto_params
from utils.system_info_osu import detect_osu_env

def run_osu_bw():
    """
    Run OSU bandwidth test (osu_bw) in single-node mode with 2 ranks.
    """
    sysinfo_raw = detect_osu_env()
    sysinfo = {
        "network": {
            "speed": sysinfo_raw["nic_speed"],
            "rdma": sysinfo_raw["rdma"],
        },
        "cpu": {"cores": sysinfo_raw["cores"]},
    }

    params = get_auto_params("osu", sysinfo)

    max_msg = params["msg_sizes"][-1]
    iterations = params["iterations"]

    cmd = f"mpirun -np 2 osu_bw -m {max_msg} -i {iterations}"

    rc, out, err = run_command(cmd)

    return {
        "tool": "osu_bw",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
