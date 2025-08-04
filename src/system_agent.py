import asyncio
import os

class SystemAgent:
    def shutdown(self):
        if os.name == 'nt':  # Windows
            os.system('shutdown /s /t 1')
        else:  # Linux and MacOS
            os.system('sudo shutdown now')
