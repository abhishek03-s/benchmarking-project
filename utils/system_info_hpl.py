import psutil
import subprocess
import math

def detect_hpl_config():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    mem = psutil.virtual_memory().total

    N = int(math.sqrt((mem * 0.80) / 8))
    NB = 192 if cores <= 32 else 256

    try:
        out = subprocess.check_output(
            "lscpu | grep 'Socket(s)'", shell=True
        ).decode()
        sockets = int(out.split(":")[1].strip())
    except Exception:
        sockets = 1

    Q = cores // sockets if sockets > 0 else cores
    P = sockets if sockets > 0 else 1

    return {
        "cores": cores,
        "threads": threads,
        "memory": mem,
        "N": N,
        "NB": NB,
        "P": P,
        "Q": Q,
    }
