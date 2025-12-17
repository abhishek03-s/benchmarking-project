from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        cores = sysinfo["cpu"]["cores"]

        return {
            "mpi_ranks": cores,
            "iterations": 1000
        }
