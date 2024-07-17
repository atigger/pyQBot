import asyncio
from os import path

import nonebot

import config
from qBot.plugins.config import init_data

if __name__ == '__main__':
    asyncio.run(init_data())
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'qBot', 'plugins'),
        'qBot.plugins'
    )
    nonebot.get_bot()
    nonebot.run()
