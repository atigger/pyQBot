import asyncio
import time

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

from qBot import api
from qBot import utils
from qBot.plugins import config
from qBot.plugins.getFortune import get_fortune
from qBot.plugins.getNews import get_news


@nonebot.scheduler.scheduled_job('cron', minute='*/10')
async def auto_fortune():
    """
    自动发送运势
    :return:
    """
    if config.ENABLE_AUTO_FORTUNE is False:
        return
    current_weekday = time.localtime().tm_wday
    cache_weekday = -1
    try:
        f = open(config.DATA_DIR + "/cache/week.cache", "r")
        cache_weekday = f.read()
        f.close()
    except Exception as e:
        f = open(config.DATA_DIR + "/cache/week.cache", "w")
        f.write(str(-1))
        f.close()
    if current_weekday == int(cache_weekday):
        return
    fortune_txt: str = await get_fortune(True)
    fortune_txt = fortune_txt.replace("\n", "", 1)
    if fortune_txt.find("获取运势失败") != -1:
        return
    bot = nonebot.get_bot()
    send_group_list = config.GROUP_LIST
    for group_id in send_group_list:
        try:
            await bot.send_group_msg(group_id=group_id,
                                     message=fortune_txt)
        except CQHttpError:
            pass
        await asyncio.sleep(5)


@nonebot.scheduler.scheduled_job('cron', hour='15', minute='0')
async def auto_fish():
    """
    自动发送摸鱼办
    :return:
    """
    if config.ENABLE_AUTO_FORTUNE is False:
        return
    file_path = config.DATA_DIR + "/cache/mofish/" + utils.get_now_date() + ".jpg"
    downLoad_tag = await utils.downLoadFile(api.FISH_URL, file_path)
    if downLoad_tag:
        await send_img_to_group(file_path)


@nonebot.scheduler.scheduled_job('cron', hour='8', minute='30')
async def auto_news():
    """
    自动发送新闻
    :return:
    """
    if config.ENABLE_AUTO_NEWS is False:
        return
    img_path = await get_news()
    if img_path == "获取新闻失败":
        return
    await send_img_to_group(img_path)


async def send_img_to_group(img_path):
    """
    发送图片到群
    :param img_path: 图片路径
    :return:
    """
    base64_data = utils.img_to_base64(img_path)
    bot = nonebot.get_bot()
    send_group_list = config.GROUP_LIST
    for group_id in send_group_list:
        try:
            await bot.send_group_msg(group_id=group_id,
                                     message="[CQ:image,file=" + base64_data + "]")
        except CQHttpError:
            pass
        await asyncio.sleep(5)
