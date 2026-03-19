import os
from pathlib import Path

from app.repository.cache_repo import set_cache
from app.services.jm_service import search, download, search_ranking_list
from app.services.pdf_service import encrypt, auto_delete
from ncatbot.core.element import MessageChain, Text, File


async def handle_jm(msg, send):
    text = msg.raw_message.strip()

    if not text.startswith("/jm"):
        return

    cmd = text.replace("/jm", "").strip()

    # 搜索
    if "搜索" in cmd:
        result = search(cmd.replace("搜索", "").strip())
        if not result:
            await send("没搜到 😢")
            return
        set_cache(msg.user_id, result)

        msg_text = "🔎 搜索结果：\n\n"
        for i, r in enumerate(result):
            msg_text += f"{i + 1}. {r['id']} | {r['title']}\n"
        msg_text += "\n👉 发送 【/jm id】 下载"
        await send(msg_text)

    # 排行榜
    elif "排行榜" in cmd:
        # 按空格分割参数
        params = cmd.replace("排行榜", "").strip().split()

        # 定义默认值和参数映射
        time_range = "全部"  # 时间范围: 全部/今天/本周/本月
        category = "全部"  # 分类: 全部/同人/单本/短篇/韩漫/美漫/3D
        sort_by = "最新"  # 排序: 最新/按最新/浏览量/图片多/点赞数/评分/评论数

        # 根据参数数量赋值
        if len(params) >= 1 and params[0]:
            time_range = params[0]
        if len(params) >= 2 and params[1]:
            category = params[1]
        if len(params) >= 3 and params[2]:
            sort_by = params[2]

        result = search_ranking_list(time_range, category, sort_by)

        msg_text = "🔎 搜索结果：\n\n"
        for i, r in enumerate(result):
            msg_text += f"{i + 1}. {r['id']} | {r['title']}\n"
        msg_text += "\n👉 发送 【/jm id】 下载"
        await send(msg_text)

    # 纯数字
    elif cmd.isdigit():
        try:
            await send("📥 正在下载，请稍等...")
            Path("download").mkdir(exist_ok=True)
            Path("download/pdf").mkdir(exist_ok=True)
            Path("download/encrypted").mkdir(exist_ok=True)
            src = f"download/pdf/{cmd}.pdf"
            dst = f"download/encrypted/{cmd}.pdf"

            download(cmd)
            if not os.path.exists(src):
                raise Exception("下载失败")

            encrypt(src, dst, cmd)
            await msg.reply(rtf=MessageChain([
                File(dst)
            ]))

            await send("密码为本子ID")
            await auto_delete(src, 0)
            await auto_delete(dst, 20)

        except Exception as e:
            await send(f"❌ 下载失败：{str(e)}")
    else:
        msg_text = ("命令：\n"
                    "/jm 纯数字\n"
                    "/jm 搜索 [搜索内容]\n"
                    "/jm 排行榜 [全部/今天/本周/本月] [全部/同人/单本/短篇/韩漫/美漫/3D] [最新/按最新/浏览量/图片多/点赞数/评分/评论数]")
        await send(msg_text)
