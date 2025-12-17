from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo: dict) -> dict:
        rdma = sysinfo.get("rdma", False)
        speed = sysinfo.get("nic_speed", 1000)

        msg_sizes = [
            1, 2, 4, 8, 16, 32, 64, 128,
            256, 512, 1024, 2048, 4096,
            8192, 16384, 32768, 65536,
            131072, 262144, 524288, 1048576,
        ]

        iterations = 10000 if speed <= 10000 else 5000

        return {
            "msg_sizes": msg_sizes,
            "iterations": iterations,
            "rdma_enabled": rdma,
        }
