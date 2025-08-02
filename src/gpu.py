from pynvml import (
    nvmlInit, 
    nvmlShutdown,
    nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetHandleByIndex, 
    NVMLError,
)

class GpuDependency:
    init = nvmlInit
    shutdown = nvmlShutdown
    get_handle_by_index = nvmlDeviceGetHandleByIndex
    get_utilization_rates = nvmlDeviceGetUtilizationRates

class Gpu:
    def __init__(self, dependency: GpuDependency, gpu_index: int = 0):
        self._dependency = dependency
        self._dependency.init()
        self._gpu_handle = dependency.get_handle_by_index(gpu_index)

    def __del__(self):
        self._dependency.shutdown()

    def get_usage(self) -> float:
        try:
            usage = self._dependency.get_utilization_rates(self._gpu_handle)
            return usage.gpu
        except NVMLError as e:
            return 0.0
    