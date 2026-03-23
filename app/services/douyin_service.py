import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

HEADERS = {
    "user-agent": "Mozilla/5.0"
}


def extract_url(text):
    urls = re.findall(r'https?://[^\s]+', text)
    return urls[0] if urls else None


def is_douyin_url(url):
    return "douyin.com" in url or "iesdouyin.com" in url


def get_real_url(short_url):
    resp = requests.get(short_url, headers=HEADERS, allow_redirects=False)
    if resp.status_code in (301, 302):
        return resp.headers.get("Location")
    return short_url


def get_video_id(url):
    """从URL中解析视频ID"""
    # 如果是短链接，需要先获取重定向后的URL
    if 'v.douyin.com' in url and HAS_REQUESTS:
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            url = response.url
        except Exception as e:
            print(f"警告: 无法解析短链接: {e}", file=sys.stderr)

    # 从URL中提取视频ID
    patterns = [
        r'/video/(\d+)',
        r'/share/video/(\d+)',
        r'aweme_id[=:](\d+)',
        r'item_ids[=:]?(\d+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_video_data(video_url):
    """获取视频数据"""
    if not HAS_REQUESTS:
        print("❌ 需要 requests 库，请安装: pip3 install requests", file=sys.stderr)
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    try:
        response = requests.get(video_url, headers=headers, timeout=15)
        html = response.text
        return extract_video_info(html)
    except Exception as e:
        print(f"获取页面失败: {e}", file=sys.stderr)
        return None


def extract_video_info(html):
    """从HTML中提取视频信息"""
    # 使用字符串方法查找视频 URL
    # 视频 URL 格式: https:\u002F\u002Faweme.snssdk.com...
    search_str = 'aweme.snssdk.com'
    idx = html.find(search_str)

    if idx > 0:
        # 向前查找 URL 开始位置
        start = html.rfind('http', 0, idx)
        if start < 0:
            start = idx - 50  # 向前最多50个字符

        # 向后查找 URL 结束位置
        end = html.find('"', idx)
        if end < 0:
            end = idx + 200  # 向后最多200个字符

        video_url = html[start:end]

        # 解码 Unicode 转义
        video_url = video_url.replace('\\u002F', '/').replace('\\u003D', '=').replace('\\u0026', '&').replace('\\u003F',
                                                                                                              '?')

        # 将 playwm 改为 play 获取无水印版本
        if 'playwm' in video_url:
            video_url = video_url.replace('playwm', 'play')

        # 提取标题
        title = "未知标题"
        desc_match = re.search(r'"desc":"([^"]+)"', html)
        if desc_match:
            title = desc_match.group(1)

        return {
            'title': title,
            'author': '未知',
            'video_urls': [video_url]
        }

    # 方法2: 查找 __INITIAL_STATE__
    initial_state_pattern = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
    match = re.search(initial_state_pattern, html, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            if 'aweme' in data or 'detail' in data:
                aweme_data = data.get('aweme', data.get('detail', {}))
                if isinstance(aweme_data, dict) and 'video' in aweme_data:
                    video_data = aweme_data['video']
                    if 'play_addr' in video_data:
                        play_addr = video_data['play_addr']
                        if 'url_list' in play_addr and play_addr['url_list']:
                            title = aweme_data.get('desc', '未知标题')
                            return {
                                'title': title,
                                'author': aweme_data.get('author', {}).get('nickname', '未知'),
                                'video_urls': play_addr['url_list']
                            }
        except Exception as e:
            pass

    # 方法3: 查找 _ROUTER_DATA
    router_pattern = r'window\._ROUTER_DATA\s*=\s*(\{.+?\});\s*</script>'
    match = re.search(router_pattern, html, re.DOTALL)
    if match:
        try:
            data_str = match.group(1)
            data_str = data_str.replace('\\u002F', '/').replace('\\u003D', '=').replace('\\u0026', '&')
            data = json.loads(data_str)

            # 深度搜索视频数据
            def find_video_data(obj):
                if isinstance(obj, dict):
                    if 'play_addr' in obj and 'desc' in obj:
                        return obj
                    for v in obj.values():
                        result = find_video_data(v)
                        if result:
                            return result
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_video_data(item)
                        if result:
                            return result
                return None

            video_data = find_video_data(data)
            if video_data:
                url_list = video_data.get('video', {}).get('play_addr', {}).get('url_list', [])
                if url_list:
                    return {
                        'title': video_data.get('desc', '未知标题'),
                        'author': video_data.get('author', {}).get('nickname', '未知'),
                        'video_urls': url_list
                    }
        except Exception as e:
            pass

    return None


def download_video(url, output_path):
    """下载视频文件"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.douyin.com/',
    }

    cmd = [
        'curl', '-L', '-o', output_path,
        '-H', f'User-Agent: {headers["User-Agent"]}',
        '-H', f'Referer: {headers["Referer"]}',
        '--progress-bar', '-#', url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        return result.returncode == 0
    except Exception as e:
        print(f"下载失败: {e}", file=sys.stderr)
        return False


async def auto_delete(path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
