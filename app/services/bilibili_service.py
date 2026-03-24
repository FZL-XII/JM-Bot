import os
import re
import time
import urllib.parse as up
from contextlib import closing

import requests

cookie = {
}
header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer': 'https://www.bilibili.com'
}

s = requests.session()


def download_bilibili_video(url):
    if 'b23.tv' in url:
        resp = s.get(url, allow_redirects=False)
        url = resp.headers.get('location', url)

    if 'video/av' in url:
        aid = re.search(r'av(\d+)', url).group(1)
        res = s.get(
            f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}',
            headers=header, cookies=cookie
        )
        data = res.json()
        url = f"https://www.bilibili.com/video/{data['data']['bvid']}"

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

    video_info = s.get(
        f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=80&otype=json',
        headers=header, cookies=cookie
    ).json()

    save_dir = "download/bilibili/"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/{int(time.time())}.mp4"

    video_url = video_info['data']['durl'][0]['url']
    with closing(s.get(video_url, headers=header, stream=True)) as response:
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(8192):
                if chunk:
                    f.write(chunk)
    return filename
