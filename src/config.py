from dataclasses import dataclass
from datetime import timedelta
import os

@dataclass
class Config:
    gpu_index: int
    span_threshold: timedelta
    heartbeat: timedelta
    interval: timedelta
    shutdown_interval: timedelta
    app_url: str

    def default():
        return Config(
            gpu_index=0,
            span_threshold=timedelta(minutes=10),
            heartbeat=timedelta(minutes=30),
            interval=timedelta(seconds=10),
            shutdown_interval=timedelta(seconds=30),
            app_url=os.getenv('APP_URL', None)
        )

    def verify(self):
        if not self.app_url:
            raise ValueError("app_url is not set")
