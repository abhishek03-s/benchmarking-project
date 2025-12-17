from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        cores = sysinfo["cpu"]["cores"]
        mem = sysinfo["memory"]["total"]

        HPL_N = int((mem * 0.75) ** 0.5)
        STREAM_array = int((mem * 0.5) / 8)

        return {
            "HPL_N": HPL_N,
            "STREAM_array_size": STREAM_array,
            "mpi_ranks": cores
        }
