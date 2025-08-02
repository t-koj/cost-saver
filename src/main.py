import asyncio
from .config import Config
from .gpu import Gpu
from .system_agent import SystemAgent
from .watcher import Watcher, WathcherDependency
from ext.message_slack import post_message

async def main():
    dependency = WathcherDependency(
        post_message=post_message,
        gpu=Gpu(Config.default().gpu_index),
        system_agent=SystemAgent()
    )
    await Watcher(Config.default(), dependency=dependency).loop()

if __name__ == "__main__":
    asyncio.run(main())
