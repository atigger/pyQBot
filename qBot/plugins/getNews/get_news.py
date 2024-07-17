import os

from qBot import untils, api
from qBot.plugins import config


async def get_news():
    """
    获取今日新闻
    """
    news_path = config.DATA_DIR + '\\cache\\news\\' + untils.get_now_date() + '.jpg'
    if os.path.exists(news_path) is False:
        downLoad_tag = await untils.downLoadFile(api.NEWS_URL, news_path)
        if downLoad_tag is False:
            return "获取新闻失败"
    return news_path
