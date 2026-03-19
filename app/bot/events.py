from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Text
from ncatbot.utils.logger import get_log

from .client import bot
from app.handlers.jm_handler import handle_jm

_log = get_log()


@bot.group_event()
async def on_group(msg: GroupMessage):
    _log.info(msg)

    async def send(text):
        await msg.reply(rtf=MessageChain([Text(text)]))

    await handle_jm(msg, send)


@bot.private_event()
async def on_private(msg: PrivateMessage):
    _log.info(msg)

    async def send(text):
        await bot.api.post_private_msg(
            msg.user_id,
            rtf=MessageChain([Text(text)])
        )

    await handle_jm(msg, send)