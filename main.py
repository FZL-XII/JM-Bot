from app.bot.client import bot

if __name__ == "__main__":
    bot.run(
        reload=False,
        enable_webui_interaction=False
    )
