import os
import re
import shutil
import subprocess
import time
import urllib.parse as up

import requests

cookie = {
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com'
}

s = requests.session()

ffmpeg_path = shutil.which("ffmpeg")


async def download_bilibili_video(url, send):
    # ===== 1. 短链处理 =====
    if 'b23.tv' in url:
        resp = s.get(url, allow_redirects=False)
        url = resp.headers.get('location', url)

    # ===== 2. AV转BV =====
    if 'video/av' in url:
        aid = re.search(r'av(\d+)', url).group(1)
        res = s.get(
            f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}',
            headers=header, cookies=cookie
        ).json()
        url = f"https://www.bilibili.com/video/{res['data']['bvid']}"

    # ===== 3. 解析BV和P =====
    parsed = up.urlparse(url)
    bvid = parsed.path.split('/')[-1]

    query = up.parse_qs(parsed.query)
    page = int(query.get('p', [1])[0]) - 1

    # ===== 4. 获取视频信息 =====
    vid = s.get(
        f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}',
        headers=header, cookies=cookie
    ).json()

    pages = vid['data']['pages']
    page = max(0, min(page, len(pages) - 1))
    cid = pages[page]['cid']

    # ===== 5. 获取DASH流 =====
    play = s.get(
        f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=127&fnval=16',
        headers=header, cookies=cookie
    ).json()

    data = play['data']

    if 'dash' not in data:
        await send("当前权限不足或登录失效")
        return

    dash = data['dash']
    video_list = dash['video']
    audio_list = dash['audio']

    # ===== 6. 选最高画质 =====
    video_list.sort(key=lambda x: x['bandwidth'], reverse=True)
    audio_list.sort(key=lambda x: x['bandwidth'], reverse=True)

    video_url = video_list[0]['baseUrl']
    audio_url = audio_list[0]['baseUrl']

    save_dir = "download/bilibili/"
    os.makedirs(save_dir, exist_ok=True)
    file_title = int(time.time())
    video_path = f"{save_dir}/{file_title}_video.m4s"
    audio_path = f"{save_dir}/{file_title}_audio.m4s"
    output_path = f"{save_dir}/{file_title}.mp4"

    download(video_url, video_path)
    download(audio_url, audio_path)

    # ===== 8. 合并 =====
    cmd = [
        ffmpeg_path,
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(video_path)
    os.remove(audio_path)

    return output_path


def download(url, path):
    with s.get(url, headers=header, stream=True) as response:
        response.raise_for_status()  # 检查请求是否成功
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 每次写入1MB
                if chunk:
                    f.write(chunk)
