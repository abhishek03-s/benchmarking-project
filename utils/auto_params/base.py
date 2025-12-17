from abc import ABC, abstractmethod

class AutoParamBase(ABC):
    @abstractmethod
    def compute(self, sysinfo: dict) -> dict:
        """
        Compute auto-parameters for a benchmark tool based on system info.
        sysinfo: dict containing CPU, memory, NIC, RDMA, etc.
        Returns: dict of parameters.
        """
        pass
