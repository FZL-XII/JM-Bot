from app.handlers.douyin_handler import handle_douyin
from app.handlers.jm_handler import handle_jm
from app.handlers.x_handler import handle_x
from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Text
from ncatbot.utils.logger import get_log

from .client import bot

_log = get_log()


@bot.group_event()
async def on_group(msg: GroupMessage):
    _log.info(msg)

    async def send(text):
        await msg.reply(rtf=MessageChain([Text(text)]))

    if msg.raw_message.strip().startswith("/jm"):
        await handle_jm(msg, send)
    elif "x.com" in msg.raw_message.strip() or "twitter.com" in msg.raw_message.strip():
        await handle_x(msg, send)
    else:
        await handle_douyin(msg)


@bot.private_event()
async def on_private(msg: PrivateMessage):
    _log.info(msg)

    async def send(text):
        await bot.api.post_private_msg(
            msg.user_id,
            rtf=MessageChain([Text(text)])
        )

    if msg.raw_message.strip().startswith("/jm"):
        await handle_jm(msg, send)
    elif "x.com" in msg.raw_message.strip() or "twitter.com" in msg.raw_message.strip():
        await handle_x(msg, send)
    else:
        await handle_douyin(msg)
