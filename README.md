# JM-Bot

QQ机器人 当前功能：

1、JM 搜索、排行榜、下载

2、抖音分享链接下载

本项目仅供学习交流使用，请勿用于非法用途。使用本项目产生的一切后果由使用者自行承担。

## 安装

1. 克隆项目

```bash
git clone https://github.com/FZL-XII/JM-Bot.git
cd JM-Bot
```

2. 安装依赖 

```bash
pip install -r requirements.txt
```

3. 下载 napcat

    下载：https://github.com/NapNeko/NapCatQQ/releases

    推荐轻量化的一键部署方案

    找到`\NapCat.Shell.Windows.OneKey\NapCat.44498.Shell\versions\9.9.26-44498\resources\app\napcat\config` 文件夹下的 `onebot11_XXXXXXX.json` 文件修改 `websocketServers` 配置

```bash 
    "websocketServers": [
      {
        "enable": true,
        "name": "websocket-server",
        "host": "127.0.0.1",
        "port": 3001,
        "reportSelfMessage": true,
        "enableForcePushEvent": true,
        "messagePostFormat": "array",
        "token": "",
        "debug": true,
        "heartInterval": 30000
      }
    ],
```
4. 运行

    `\NapCat.Shell.Windows.OneKey\NapCat.44498.Shell` 文件夹下 `napcat.bat`启动

    更改 `client.py` 各参数，运行 `start.bat` 

## 命令
/jm 纯数字

/jm 搜索 [搜索内容]

/jm 排行榜 [全部/今天/本周/本月] [全部/同人/单本/短篇/韩漫/美漫/3D] [最新/按最新/浏览量/图片多/点赞数/评分/评论数]

## 参考

- [NapCatQQ](https://napcat.napneko.icu/)
- [NcatBot](https://docs.ncatbot.xyz/)
- [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python)