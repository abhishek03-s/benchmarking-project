from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        speed = sysinfo["network"]["speed"]

        if speed >= 100_000:
            parallel = 16
        elif speed >= 40_000:
            parallel = 8
        else:
            parallel = 4

        return {
            "parallel_streams": parallel,
            "duration": 10
        }
