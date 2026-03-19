import asyncio
from pathlib import Path

import pikepdf
from jmcomic import *
from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Text, File
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

# 基础配置
config.set_bot_uin("2517824720")
config.set_root("")
config.set_ws_uri("ws://localhost:3001")
config.set_token("")

bot = BotClient()
_log = get_log()

# jm 配置
loadConfig = JmOption.from_file("config.yml")
client = JmOption.default().new_jm_client()

# 搜索缓存（防止串人）
search_cache = {}


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


# 下载
def download_jm(album_id):
    loadConfig.download_album([album_id])


# 公共方法
async def handle_jm(msg, user_id, send_func):
    text = msg.raw_message.strip()

    if not text.startswith("/jm"):
        return

    cmd = text.replace("/jm", "").strip()

    # ================= 搜索 =================
    if not cmd.isdigit():
        result = search_jm(cmd)

        if not result:
            await send_func("没搜到 😢")
            return

        search_cache[user_id] = result

        msg_text = "🔎 搜索结果：\n\n"
        for i, r in enumerate(result):
            msg_text += f"{i + 1}. {r['id']} | {r['title']}\n"

        msg_text += "\n👉 发送 /jm id 下载"

        await send_func(msg_text)
        return

    # 下载
    album_id = cmd

    try:
        await send_func("📥 正在下载，请稍等...")
        Path("pdf").mkdir(exist_ok=True)
        Path("encrypted").mkdir(exist_ok=True)
        download_jm(album_id)
        file_path = f"pdf/{album_id}.pdf"
        encrypted_file_path = f"encrypted/{album_id}.pdf"
        password = f"{album_id}"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"下载失败：文件 {file_path} 不存在")

        with pikepdf.open(file_path) as pdf:
            pdf.save(encrypted_file_path,
                     encryption=pikepdf.Encryption(
                         user=password,  # 用户密码
                         owner=password,  # 所有者密码
                         R=4,  # 加密算法版本
                     ))

        print(f"加密完成: {encrypted_file_path}")

        # 删除原始未加密文件
        await delete_file_after_delay(file_path, 0)
        print(f"已删除原始文件: {file_path}")

        await msg.reply(rtf=MessageChain([
            File(encrypted_file_path)
        ]))
        await send_func("密码为本子ID")

        await delete_file_after_delay(encrypted_file_path, 20)
    except Exception as e:
        await send_func(f"❌ 下载失败：{str(e)}")


async def delete_file_after_delay(file_path, delay_seconds):
    await asyncio.sleep(delay_seconds)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ 已自动删除文件: {file_path}")
    except Exception as e:
        print(f"❌ 删除文件失败: {e}")


# 群消息
@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)

    async def send(text):
        await msg.reply(rtf=MessageChain([Text(text)]))

    await handle_jm(msg, msg.user_id, send)


# 私聊消息
@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)

    async def send(text):
        await bot.api.post_private_msg(
            msg.user_id,
            rtf=MessageChain([Text(text)])
        )

    await handle_jm(msg, msg.user_id, send)


# 启动
if __name__ == "__main__":
    bot.run(
        reload=False,
        enable_webui_interaction=False
    )
