from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        speed = sysinfo["network"]["speed"]

        max_msg = 4 * 1024 * 1024 if speed >= 40_000 else 1 * 1024 * 1024

        return {
            "max_message_size": max_msg
        }
