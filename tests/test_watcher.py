from gpu import Gpu
from system_agent import SystemAgent
from watcher import Watcher, WatcherDependency
from datetime import timedelta
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, create_autospec
from config import Config

@pytest.fixture
def watcher():
    config = Config.default()
    dependency = WatcherDependency(
        post_message=AsyncMock(),
        gpu=create_autospec(Gpu, instance=True),
        system_agent=create_autospec(SystemAgent, instance=True)
    )
    return Watcher(config=config, dependency=dependency)

def test_watcher_initialization(watcher):
    assert watcher._config is not None
    assert watcher._dependency is not None
    assert isinstance(watcher._dependency.post_message, AsyncMock)
    assert isinstance(watcher._dependency.gpu, Gpu)
    assert isinstance(watcher._dependency.system_agent, SystemAgent)
    assert watcher._start_time is not None
    assert watcher._last_active == watcher._start_time
    assert watcher._last_heartbeat == watcher._start_time

@pytest.mark.asyncio
async def test_post(watcher):
    message = "Test message"
    await watcher.post(message=message)
    watcher._dependency.post_message.assert_awaited_with(message)

@pytest.mark.asyncio
async def test_time_left_to_shutdown(watcher):
    watcher._dependency.gpu.get_usage.return_value = 50
    time_left = await watcher.time_left_to_shutdown()
    assert isinstance(time_left, timedelta)

@pytest.mark.asyncio
async def test_shutdown(watcher):
    watcher._config.shutdown_interval = timedelta(seconds=1)
    await watcher._shutdown()
    watcher._dependency.system_agent.shutdown.assert_awaited_once()

@pytest.mark.asyncio
async def test_post_heartbeat_every_interval(watcher):
    watcher._config.heartbeat = timedelta(seconds=1)
    watcher._last_heartbeat = watcher._start_time - timedelta(seconds=2)
    await watcher._post_heartbeat_every_interval()
    watcher._dependency.post_message.assert_awaited_once()

def test_get_running_time_in_minutes(watcher):
    running_time = watcher._get_running_time_in_minutes()
    assert isinstance(running_time, float)
    assert running_time >= 0
    
@pytest.mark.asyncio
async def test_loop(watcher):
    watcher._config.app_url = "http://example.com"
    watcher._config.interval = timedelta(seconds=0.1)
    watcher._config.span_threshold = timedelta(seconds=1)
    watcher._config.shutdown_interval = timedelta(seconds=1)
    
    watcher._dependency.gpu.get_usage.return_value = 0
    watcher._dependency.system_agent.shutdown = AsyncMock()
    
    watcher._test = True
    await watcher.loop()

    watcher._dependency.post_message.assert_awaited()
    assert watcher._last_active < watcher._start_time + timedelta(seconds=1)

@pytest.mark.asyncio
async def test_loop_shutdown(watcher):
    watcher._config.app_url = "http://example.com"
    watcher._config.interval = 0.1
    watcher._config.span_threshold = timedelta(seconds=1)
    watcher._config.shutdown_interval = timedelta(seconds=1)
    watcher.time_left_to_shutdown = AsyncMock(return_value=timedelta(seconds=-1))
    watcher._test = True
    await watcher.loop()

    watcher._dependency.system_agent.shutdown.assert_awaited_once()
    assert watcher._last_active < watcher._start_time + timedelta(seconds=1)

@pytest.mark.asyncio
async def test_loop_shutdown_warning(watcher):
    watcher._config.app_url = "http://example.com"
    watcher._config.interval = timedelta(seconds=0.1)
    watcher._config.span_threshold = timedelta(seconds=1)
    watcher._config.shutdown_interval = timedelta(seconds=1)

    watcher._shutdown = AsyncMock(side_effect=Exception("Test exception"))
    watcher._dependency.gpu.get_usage.return_value = 0
    watcher._test = False

    with pytest.raises(Exception):
        await watcher.loop()
