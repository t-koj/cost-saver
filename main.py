import asyncio
from src import Config, Gpu, GpuDependency, SystemAgent, Watcher, WatcherDependency
from ext.message_slack import post_message

async def main():
    watcher_depenency = WatcherDependency(
        post_message=post_message,
        gpu=Gpu(GpuDependency.default(), Config.default().gpu_index),
        system_agent=SystemAgent()
    )
    watcher = Watcher(
        config=Config.default(),
        dependency=watcher_depenency
    )
    await watcher.loop()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(main())
