from utils.auto_params.base import AutoParamBase
import math

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        cores = sysinfo["cpu"]["cores"]
        mem = sysinfo["memory"]["total"]
        sockets = sysinfo["cpu"]["sockets"]

        N = int(math.sqrt((mem * 0.80) / 8))
        NB = 192 if cores <= 32 else 256

        P = sockets
        Q = cores // sockets

        return {
            "N": N,
            "NB": NB,
            "P": P,
            "Q": Q
        }
