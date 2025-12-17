# runners/iperf3_runner.py

from utils.shell import run_command
from utils.auto_params.engine import get_auto_params

def _get_sysinfo():
    # For loopback, we can treat speed as an arbitrary high value or a default
    return {
        "network": {
            "speed": 10000,  # Mb/s (logical assumption for localhost scenario)
        }
    }

def run_iperf3():
    """
    Single-node iperf3 scenario using loopback (localhost).
    Server is launched implicitly; if you want proper client/server,
    you'd run a server separately.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("iperf3", sysinfo)

    parallel = params["parallel_streams"]
    duration = params["duration"]

    # For a robust setup, you might start a background iperf3 -s, but
    # here we assume the user has a server running or uses localhost
    cmd = f"iperf3 -c 127.0.0.1 -P {parallel} -t {duration}"

    rc, out, err = run_command(cmd)

    return {
        "tool": "iperf3",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
    }
