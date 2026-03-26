import time

from ncatbot.core.element import MessageChain, File

from app.services.x_service import download_twitter_video
from app.utils.util import auto_delete, zip_single_video


async def handle_x(msg, send):
    url = msg.raw_message
    userId = msg.user_id
    if not url:
        return

    output_path = download_twitter_video(url)

    if not output_path:
        return

    output_zip = f"download/encrypted/{int(time.time())}.zip"
    zip_single_video(output_path, output_zip, str(userId))

    # 发送视频文件
    await msg.reply(rtf=MessageChain([
        File(output_zip)
    ]))

    await send("密码为你的QQ号")
    await auto_delete(output_path)
    await auto_delete(output_zip, 20)
