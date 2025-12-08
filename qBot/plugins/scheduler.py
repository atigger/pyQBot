import asyncio
import os
import time

import nonebot
import httpx
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot import logger

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
        f = open(os.path.join(config.DATA_DIR, 'cache', 'week.cache'), "r")
        cache_weekday = f.read()
        f.close()
    except Exception as e:
        f = open(os.path.join(config.DATA_DIR, 'cache', 'week.cache'), "w")
        f.write(str(-1))
        f.close()
    if current_weekday == int(cache_weekday):
        return
    fortune_txt: str = await get_fortune()
    fortune_txt = fortune_txt.replace("\n", "", 1)
    if fortune_txt.find("获取运势失败") != -1:
        return
    f = open(os.path.join(config.DATA_DIR, 'cache', 'week.cache'), "w")
    f.write(str(current_weekday))
    f.close()
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
    file_path = os.path.join(config.DATA_DIR, 'cache', 'mofish', utils.get_now_date() + ".jpg")
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


# 存储上次通知时间的全局变量
last_offline_notification_time = 0
# 记录机器人启动时间
bot_startup_time = time.time()


async def send_notification(message, title, tags):
    """
    发送通知
    :param message: 通知内容
    :param title: 通知标题
    :param tags: 通知标签
    :return:
    """
    url = config.NOTIFICATION_API_URL

    # 检查API URL是否配置
    if not url or url.strip() == '':
        logger.warning("通知API URL未配置，跳过发送通知")
        return

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "title": title,
        "desp": message,
        "tags": tags
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code == 200:
                logger.info("通知发送成功")
            else:
                logger.error(f"通知发送失败: {response.status_code}")
    except Exception as e:
        logger.error(f"发送通知时发生错误: {e}")


@nonebot.scheduler.scheduled_job('cron', minute='*')
async def check_bot_online():
    """
    每分钟检查机器人是否在线
    如果离线且距离上次通知超过30分钟，则发送通知
    :return:
    """
    global last_offline_notification_time, bot_startup_time

    # 检查是否启用机器人监控功能
    if not config.ENABLE_BOT_MONITOR:
        return

    # 启动后60秒内不进行检测，给机器人足够的初始化时间
    current_time = time.time()
    if (current_time - bot_startup_time) < 60:
        logger.debug(f"机器人启动中，跳过在线检测（剩余 {60 - (current_time - bot_startup_time):.0f} 秒）")
        return

    try:
        bot = nonebot.get_bot()
        # 尝试获取bot信息来检查是否在线
        await bot.get_login_info()
        # 如果执行到这里说明bot在线，重置通知时间
        if last_offline_notification_time > 0:
            logger.info("机器人恢复在线状态")
            last_offline_notification_time = 0
    except Exception as e:

        # 检查是否需要发送通知（30分钟 = 1800秒）
        if last_offline_notification_time == 0 or (current_time - last_offline_notification_time) >= 1800:
            # 发送离线通知
            offline_message = f"机器人离线检测\n时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n状态: 机器人已离线\n错误信息: {str(e)}"
            await send_notification(
                message=offline_message,
                title="机器人离线警告",
                tags="机器人状态"
            )
            last_offline_notification_time = current_time
            logger.warning(f"机器人离线，已发送通知: {e}")
        else:
            logger.debug(f"机器人仍然离线，距离下次通知还有 {1800 - (current_time - last_offline_notification_time):.0f} 秒")

