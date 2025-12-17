from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        cores = sysinfo["cpu"]["cores"]
        mem = sysinfo["memory"]["total"]

        transfer = "1m"
        block = "4m"
        file_size = int(mem * 0.5)

        return {
            "transfer_size": transfer,
            "block_size": block,
            "mpi_ranks": cores,
            "file_size": file_size
        }
