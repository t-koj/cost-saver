from unittest.mock import MagicMock
import pytest
from gpu import Gpu, GpuDependency
from pynvml import NVMLError

@pytest.fixture
def gpu():
    gpu_dependency = MagicMock(spec=GpuDependency)
    gpu = Gpu(gpu_dependency)
    return gpu

def test_gpu_initialization(gpu):
    assert gpu._gpu_handle is not None

def test_gpu_get_usage(gpu):
    # Mock the return value of get_utilization_rates
    mock_usage = MagicMock()
    mock_usage.gpu = 42.0
    gpu._dependency.get_utilization_rates.return_value = mock_usage

    usage = gpu.get_usage()
    assert usage == 42.0
    gpu._dependency.get_utilization_rates.assert_called_once_with(gpu._gpu_handle)

def test_gpu_get_usage_handles_exception(gpu):
    # Simulate NVMLError being raised
    gpu._dependency.get_utilization_rates.side_effect = NVMLError("error")
    usage = gpu.get_usage()
    assert usage == 0.0

def test_gpu_shutdown_called_on_del(gpu):
    del gpu