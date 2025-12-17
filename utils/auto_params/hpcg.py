from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        cores = sysinfo["cpu"]["cores"]

        nx = ny = nz = 128 if cores > 32 else 64

        return {
            "nx": nx,
            "ny": ny,
            "nz": nz
        }
