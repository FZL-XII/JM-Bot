import os
import time
from pathlib import Path

import yt_dlp


def download_twitter_video(url):
    # 网址
    twitter_url = url.replace("x.com", "twitter.com")

    # 创建保存目录
    save_dir = "download/X/"
    os.makedirs("download", exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)

    # 读取cookies
    script_dir = Path(__file__).resolve().parents[2]  # 根据层级调整
    cookies_file = script_dir / "config" / "cookies.txt"

    ydl_opts = {
        'cookiefile': cookies_file,
        'format': 'best[ext=mp4]',
        'outtmpl': os.path.join(save_dir, f'{int(time.time())}.80s.%(ext)s'),
        'noplaylist': True,
        'retries': 3,
        'quiet': True,  # 不打印 yt-dlp 自带日志
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(twitter_url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"文件已保存到: {filename}")
        return filename

    except Exception as e:
        print(f"\n❌ 下载失败: {str(e)}")
        return None
