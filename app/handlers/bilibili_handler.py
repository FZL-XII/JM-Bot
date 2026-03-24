import html
import json
import re

from ncatbot.core.element import MessageChain, File

from app.services.bilibili_service import download_bilibili_video
from app.utils.util import auto_delete


async def handle_bilibili(msg):
    # 1️⃣ 提取 data 部分
    m = re.search(r'\[CQ:json,data=(.*)\]', msg.raw_message, re.S)
    if not m:
        return
    data_str = m.group(1)
    data_str = html.unescape(data_str)
    data = json.loads(data_str)
    url = data['meta']['detail_1']['qqdocurl']

    if not url:
        return

    output_path = download_bilibili_video(url)

    if not output_path:
        return

    # 发送视频文件
    await msg.reply(rtf=MessageChain([
        File(output_path)
    ]))

    await auto_delete(output_path, 20)
