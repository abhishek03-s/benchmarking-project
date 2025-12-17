import subprocess
import psutil

def detect_osu_env():
    cores = psutil.cpu_count(logical=False)

    try:
        out = subprocess.check_output(
            "ethtool eth0 | grep Speed", shell=True
        ).decode()
        nic_speed = int(out.split(":")[1].strip().replace("Mb/s", ""))
    except Exception:
        nic_speed = 1000

    try:
        subprocess.check_output("ibv_devinfo", shell=True, stderr=subprocess.DEVNULL)
        rdma = True
    except Exception:
        rdma = False

    return {
        "cores": cores,
        "nic_speed": nic_speed,
        "rdma": rdma,
    }
