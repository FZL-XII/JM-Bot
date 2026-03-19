from ncatbot.core import BotClient
from ncatbot.utils.config import config

config.set_bot_uin("2517824720")
config.set_root("")
config.set_ws_uri("ws://localhost:3001")
config.set_token("")

bot = BotClient()

# 必须 import 才会注册事件
from . import events
