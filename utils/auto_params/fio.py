from utils.auto_params.base import AutoParamBase

class AutoParams(AutoParamBase):
    def compute(self, sysinfo):
        disk_type = sysinfo["storage"]["type"]
        mem = sysinfo["memory"]["total"]

        if disk_type == "nvme":
            bs = "128k"
            iodepth = 64
        else:
            bs = "64k"
            iodepth = 16

        filesize = int(mem * 0.25)

        return {
            "block_size": bs,
            "iodepth": iodepth,
            "filesize": filesize
        }
