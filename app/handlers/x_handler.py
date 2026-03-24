import time

from app.services.x_service import download_twitter_video
from app.utils.util import auto_delete, zip_single_video
from ncatbot.core.element import MessageChain, Text, File


async def handle_x(msg, send):
    url = msg.raw_message

    if not url:
        return

    output_path = download_twitter_video(url)

    if not output_path:
        return

    password = int(time.time())
    output_zip = f"download/encrypted/{password}.zip"
    zip_single_video(output_path, output_zip, str(password))

    # 发送视频文件
    await msg.reply(rtf=MessageChain([
        File(output_zip)
    ]))

    await send("密码为文件名")
    await auto_delete(output_path, 0)
    await auto_delete(output_zip, 20)
