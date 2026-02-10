from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession

from qBot import api


@on_command('news', aliases=('新闻', '今日新闻'))
async def _(session: CommandSession):
    """
    获取今日新闻
    """
    try:
        await session.send(MessageSegment.image(api.NEWS_URL))
        return
    except:
        pass
    await session.send('获取新闻失败')
