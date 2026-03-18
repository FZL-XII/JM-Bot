# JM-Bot

基于 Napcat, NcatBot, JMComic-Crawler-Python 的 QQ 机器人。

## Install

1. 克隆项目

```bash
git clone https://github.com/FZL-XII/JM-Bot.git
cd JM-Bot
```

2. 安装依赖 

```bash
pip install -r requirements.txt`
```

3. 下载 napcat

下载：https://github.com/NapNeko/NapCatQQ/releases

推荐轻量化的一键部署方案

找到`\NapCat.Shell.Windows.OneKey\NapCat.44498.Shell\versions\9.9.26-44498\resources\app\napcat\config` 文件夹下的 `onebot11_XXXXXXX.json`文件修改配置

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

更改 `main.py` 各参数，运行 `python main.py`，接下来按照指示操作。

## Usage

输入 /jm <id:xxx> ，机器人会自动下载生成 pdf 并发送消息。

例： /jm 350234

输入 /jm <中文> ，机器人会自动搜索并发送消息。

例： /jm 中文

## Reference

- [NapCatQQ](https://napcat.napneko.icu/)
- [NcatBot](https://docs.ncatbot.xyz/)
- [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python)