
from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        mem = sysinfo["memory"]["total"]
        cores = sysinfo["cpu"]["cores"]

        array_size = int((mem * 0.5) / 8)

        return {
            "array_size": array_size,
            "threads": cores
        }
