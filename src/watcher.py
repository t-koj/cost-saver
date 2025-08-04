import asyncio
from datetime import timedelta, datetime
from time import time
from config import Config
from gpu import Gpu
from system_agent import SystemAgent
from typing import Callable, Awaitable

class WatcherDependency:
    def __init__(self, post_message: Callable[[str], Awaitable[None]], gpu: Gpu, system_agent: SystemAgent):
        self.post_message = post_message
        self.gpu = gpu
        self.system_agent = system_agent

class Watcher:
    def __init__(self, *, config: Config, dependency: WatcherDependency):
        self._post_message = dependency.post_message
        self._dependency = dependency
        self._config = config
        self._start_time = datetime.now()
        self._last_active = self._start_time
        self._last_heartbeat = self._start_time
        self._test = None

    async def post(self, message: str):
        await self._dependency.post_message(message)

    async def time_left_to_shutdown(self) -> timedelta:
        usage = self._dependency.gpu.get_usage()
        if usage > 0:
            self._last_active = datetime.now()
        inactive_span = datetime.now() - self._last_active
        return self._config.span_threshold - inactive_span
    
    async def _shutdown(self):
        await self.post('Shutting down..')
        self._dependency.system_agent.shutdown()
    
    async def _post_heartbeat_every_interval(self):
        now = datetime.now()
        after_heartbeat = now - self._last_heartbeat
        if after_heartbeat > self._config.heartbeat:
            self._last_heartbeat = now
            await self.post(
                f'Running for {self._get_running_time_in_minutes():.0f} minutes'
            )

    def _get_running_time_in_minutes(self):
        return (datetime.now() - self._start_time).total_seconds() / 60

    async def loop(self):
        try:
            while True:
                await self._post_heartbeat_every_interval()
                left = await self.time_left_to_shutdown()
                if left < timedelta(seconds=0):
                    await self._shutdown()
                    await asyncio.sleep(self._config.shutdown_interval.total_seconds())
                elif left < timedelta(seconds=65):
                    await self.post(f'Shutdown in 1 minute..')
                    await asyncio.sleep(self._config.interval.total_seconds())
                else:
                    await asyncio.sleep(self._config.interval.total_seconds())
                if self._test:
                    break
        except Exception as e:
            await self.post(f"Error: {e}")
            raise
    