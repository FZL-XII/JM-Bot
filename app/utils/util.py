import asyncio
import os
 

async def auto_delete(path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
