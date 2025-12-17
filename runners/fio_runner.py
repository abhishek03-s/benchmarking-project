# runners/fio_runner.py

import os
import psutil
from utils.shell import run_command
from utils.auto_params.engine import get_auto_params

def _get_sysinfo():
    # You can later extend this to actually detect storage type via lsblk
    return {
        "memory": {"total": psutil.virtual_memory().total},
        "storage": {"type": "nvme"},  # placeholder; refine later
    }

def run_fio(target_dir: str = "/tmp"):
    """
    Run FIO on a single node.
    Scenario: random RW test against a file on the target directory.
    """
    sysinfo = _get_sysinfo()
    params = get_auto_params("fio", sysinfo)

    bs = params["block_size"]
    iodepth = params["iodepth"]
    filesize_bytes = params["filesize"]
    filesize_mb = max(1, filesize_bytes // (1024 * 1024))

    os.makedirs(target_dir, exist_ok=True)
    filename = os.path.join(target_dir, "fio_test_file")

    cmd = (
        f"fio --name=randrw "
        f"--filename={filename} "
        f"--rw=randrw --rwmixread=70 "
        f"--bs={bs} --iodepth={iodepth} "
        f"--size={filesize_mb}M --numjobs=1 "
        f"--time_based --runtime=30 "
        f"--group_reporting"
    )

    rc, out, err = run_command(cmd)

    return {
        "tool": "fio",
        "cmd": cmd,
        "return_code": rc,
        "stdout": out,
        "stderr": err,
        "params": params,
        "sysinfo": sysinfo,
        "target_dir": target_dir,
    }
