from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Text
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

from app.handlers.bilibili_handler import handle_bilibili
from app.handlers.douyin_handler import handle_douyin
from app.handlers.jm_handler import handle_jm
from app.handlers.x_handler import handle_x

# ===== 配置 =====
config.set_bot_uin("")
config.set_root("")
config.set_ws_uri("ws://localhost:3001")
config.set_token("")

bot = BotClient()
_log = get_log()


# ===== 公共逻辑（核心优化点）=====
async def handle_message(msg, send):
    text = msg.raw_message.strip()

    if text.startswith("/jm"):
        await handle_jm(msg, send)
    elif "x.com" in text or "twitter.com" in text:
        await handle_x(msg, send)
    elif "video/av" in text or "b23.tv" in text:
        await handle_bilibili(msg, send)
    else:
        await handle_douyin(msg)


# ===== 群消息 =====
@bot.group_event()
async def on_group(msg: GroupMessage):
    _log.info(msg)

    async def send(text):
        await msg.reply(rtf=MessageChain([Text(text)]))

    await handle_message(msg, send)


# ===== 私聊消息 =====
@bot.private_event()
async def on_private(msg: PrivateMessage):
    _log.info(msg)

    async def send(text):
        await bot.api.post_private_msg(
            msg.user_id,
            rtf=MessageChain([Text(text)])
        )

    await handle_message(msg, send)
