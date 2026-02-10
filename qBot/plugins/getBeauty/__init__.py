import json

import requests
from aiocqhttp import MessageSegment
from nonebot import CommandSession, on_command

from qBot import api


@on_command('beauty', aliases=('美女', '美女图片'))
async def _(session: CommandSession):
    """
    以单张图片的形式发送美女图片
    """
    r = requests.get(api.BEAUTY_URL, timeout=10)
    if r.status_code == 200:
        data = r.content
        url_data = json.loads(data)['text']
        await session.send(message=MessageSegment.image(url_data))
    else:
        await session.send('获取图片失败')
