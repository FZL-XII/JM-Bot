import time
from pathlib import Path

from ncatbot.core.element import MessageChain, File

from app.services.douyin_service import extract_url, is_douyin_url, get_real_url
from app.services.douyin_service import get_video_id, fetch_video_data, download_video
from app.utils.util import auto_delete


async def handle_douyin(msg):
    text = msg.raw_message

    url = extract_url(text)
    if not url:
        return

    if not is_douyin_url(url):
        return

    real_url = get_real_url(url)
    video_id = get_video_id(real_url)

    if not video_id:
        await msg.reply("分享链接有误")
        return

    share_url = f"https://www.iesdouyin.com/share/video/{video_id}/"
    video_info = fetch_video_data(share_url)
    if not video_info or not video_info['video_urls']:
        await msg.reply("分享链接有误")
        return

    video_urls = video_info['video_urls']
    no_watermark_url = None
    watermarked_url = None
    for url in video_urls:
        if '/playwm/' in url:
            watermarked_url = url
        elif '/play/' in url:
            no_watermark_url = url

    # 优先下载无水印版本
    download_url = no_watermark_url or watermarked_url or video_urls[0]

    Path("download").mkdir(exist_ok=True)
    Path("download/douyin").mkdir(exist_ok=True)
    output_path = f"download/douyin/{int(time.time())}.mp4"
    success = download_video(download_url, str(output_path))

    if success:
        # 发送视频文件
        await msg.reply(rtf=MessageChain([
            File(output_path)
        ]))

        await auto_delete(output_path, 20)
    else:
        await msg.reply("下载失败")
