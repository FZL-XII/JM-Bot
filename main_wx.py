import asyncio
import json
import time
from pathlib import Path

import itchat
import requests
from itchat.content import *
from jmcomic import *


# 搜索
def search_jm(keyword):
    page = client.search_site(keyword, 1)
    result = []

    for album_id, title in page:
        result.append({
            "id": album_id,
            "title": title
        })

    return result[:10]


def get_response(msg):
    try:
        text = msg.raw_message.strip()

        if not text.startswith("/jm"):
            return

        cmd = text.replace("/jm", "").strip()

        if not cmd.isdigit():
            result = search_jm(cmd)

            if not result:
                return

            search_cache[user_id] = result

            msg_text = "🔎 搜索结果：\n\n"
            for i, r in enumerate(result):
                msg_text += f"{i + 1}. {r['id']} | {r['title']}\n"

            msg_text += "\n👉 发送 /jm id 下载"

            return msg_text
    except:
        return


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def handle_group_msg(msg):
    text = msg['Text']
    user_id = msg['FromUserName']

    reply = get_response(text)

    if reply:
        itchat.send(reply, toUserName=user_id)


itchat.auto_login(hotReload=True)
itchat.run()
