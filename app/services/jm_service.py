from jmcomic import *

option = JmOption.from_file("config.yml")
client = JmOption.default().new_jm_client()


def search(keyword):
    page = client.search_site(keyword, 1)
    result = []

    for album_id, title in page:
        result.append({
            "id": album_id,
            "title": title
        })

    return result[:10]


def download(album_id):
    option.download_album([album_id])


TIME_MAP = {
    "今天": "t",
    "按今天": "t",
    "本日": "t",

    "本周": "w",
    "按本周": "w",
    "最近一周": "w",

    "本月": "m",
    "按本月": "m",
    "最近一月": "m",

    "全部": "a",
    "不限时间": "a",
    "所有时间": "a"
}


def get_time_code(name: str):
    code = TIME_MAP.get(name)
    if not code:
        return "t"
    return code


CATEGORY_MAP = {
    "全部": "0",
    "同人": "doujin",
    "单本": "single",
    "短篇": "short",
    "其他": "another",
    "韩漫": "hanman",
    "韩国": "hanman",
    "韩": "hanman",
    "美漫": "meiman",
    "美国": "meiman",
    "cosplay": "doujin_cosplay",
    "3D": "3D",
    "英文站": "english_site",
    "英文": "english_site"
}


def get_category_code(name: str):
    code = CATEGORY_MAP.get(name)
    if not code:
        return "0"
    return code


ORDER_BY_MAP = {
    "最新": "mr",
    "按最新": "mr",
    "浏览量": "mv",
    "按浏览量": "mv",
    "图片多": "mp",
    "按图片数": "mp",
    "点赞数": "tf",
    "按点赞": "tf",
    "评分": "tr",
    "按评分": "tr",
    "评论数": "md",
    "按评论": "md"
}


def get_order_by_code(name: str):
    code = ORDER_BY_MAP.get(name)
    if not code:
        return "mr"
    return code


def search_ranking_list(timeStr, categoryStr, orderByStr):
    time_code = get_time_code(timeStr)
    category_code = get_category_code(categoryStr)
    order_by_code = get_order_by_code(orderByStr)

    page = client.categories_filter(
        page=1,
        time=time_code,
        category=category_code,
        order_by=order_by_code,
    )

    result = []
    for aid, title in page:
        result.append({
            "id": aid,
            "title": title
        })

    return result[:10]
