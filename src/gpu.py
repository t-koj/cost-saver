from typing import Any, Callable
from pynvml import (
    nvmlInit, 
    nvmlShutdown,
    nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetHandleByIndex, 
    NVMLError,
)

class GpuDependency:
    init: Callable[[], None]
    shutdown: Callable[[], None]
    get_handle_by_index: Callable[[int], Any]
    get_utilization_rates: Callable[[Any], Any]

    @staticmethod
    def default() -> 'GpuDependency':
        d = GpuDependency()
        d.init = nvmlInit
        d.shutdown = nvmlShutdown
        d.get_handle_by_index = nvmlDeviceGetHandleByIndex
        d.get_utilization_rates = nvmlDeviceGetUtilizationRates
        return d

class Gpu:
    def __init__(self, dependency: GpuDependency, gpu_index: int = 0):
        self._dependency = dependency
        self._dependency.init()
        self._gpu_handle = dependency.get_handle_by_index(gpu_index)

    def __del__(self):
        try:
            self._dependency.shutdown()
        except Exception:
            pass

    def get_usage(self) -> float:
        try:
            usage = self._dependency.get_utilization_rates(self._gpu_handle)
            return usage.gpu
        except NVMLError as e:
            return 0.0
    