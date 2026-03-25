from ncatbot.core.element import MessageChain, File

from app.services.bilibili_service import extract_url, download_bilibili_video
from app.utils.util import auto_delete


async def handle_bilibili(msg, send):
    url = extract_url(msg)

    if not url:
        return

    output_path = download_bilibili_video(url)

    if not output_path:
        await send("下载失败")
        return

    # 发送视频文件
    await msg.reply(rtf=MessageChain([
        File(output_path)
    ]))

    await auto_delete(output_path, 20)
