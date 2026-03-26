import yaml
from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.core.element import MessageChain, Text
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

from app.handlers.bilibili_handler import handle_bilibili
from app.handlers.douyin_handler import handle_douyin
from app.handlers.jm_handler import handle_jm
from app.handlers.x_handler import handle_x


def load_config(path="jm_config.yml"):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    bot_cfg = data.get("jm-bot", {})

    config.set_bot_uin(bot_cfg.get("uin", ""))
    config.set_root(bot_cfg.get("root", ""))
    config.set_ws_uri(bot_cfg.get("ws_uri", ""))
    config.set_token(bot_cfg.get("token", ""))


# 先加载配置
load_config()

# 再初始化 bot
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
