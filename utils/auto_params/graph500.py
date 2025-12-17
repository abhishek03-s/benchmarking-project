from utils.auto_params.base import AutoParamBase
import math

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        mem = sysinfo["memory"]["total"]

        scale = int(math.log2(mem / (8 * 1024 * 1024)))
        edge_factor = 16

        return {
            "scale": scale,
            "edge_factor": edge_factor
        }
