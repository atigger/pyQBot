from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession

from qBot import untils
from qBot.plugins.getNews.get_news import get_news


@on_command('news', aliases=('新闻', '今日新闻'))
async def news(session: CommandSession):
    """
    获取今日新闻
    """
    news_txt = await get_news()
    if news_txt.find('获取新闻失败') == -1:
        try:
            await session.send(MessageSegment.image(untils.img_to_base64(news_txt)))
            return
        except:
            pass
    await session.send('获取新闻失败')
