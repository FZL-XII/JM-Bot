import asyncio
import os

import pikepdf


def encrypt(src, dst, password):
    with pikepdf.open(src) as pdf:
        pdf.save(
            dst,
            encryption=pikepdf.Encryption(
                user=password,
                owner=password,
                R=4,
            )
        )


async def auto_delete(path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
