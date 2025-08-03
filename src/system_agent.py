import asyncio
import os

class SystemAgent:
    async def shutdown(self):
        if os.name == 'nt':  # Windows
            os.system('shutdown /s /t 1')
        else:  # Linux and MacOS
            os.system('sudo shutdown now')
        await asyncio.sleep(self._config.shutdown_interval.total_seconds())
