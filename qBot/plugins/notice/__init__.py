import random
from urllib.parse import quote

import nonebot
from aiocqhttp import MessageSegment
from nonebot import on_notice, NoticeSession, logger

from qBot import utils

pokeList = ["breakdown", "bite", "cast", "crawl", "dont_touch", "eat", "hammer", "knock", "pat", "petpet", "play",
            "pound", "roll", "suck", "tear", "thump", "tightly"]


@on_notice('notify')
async def _(session: NoticeSession):
    if session.event.sub_type == 'poke':
        logger.info('有人戳我：%s', session.event)
        if session.event.target_id == session.self_id:
            base_url = 'http://q.qlogo.cn/g?b=qq&nk=' + str(session.event.user_id) + '&s=640'
            img_file_path = await utils.generate_picture_url(random.choice(pokeList), quote(base_url), 'gif')
            if img_file_path == "":
                await session.send(MessageSegment.at(session.event.user_id) + "\n你戳我干啥")
                return
            await session.send(MessageSegment.image(img_file_path))
    logger.info('有新的通知事件：%s', session.event)
