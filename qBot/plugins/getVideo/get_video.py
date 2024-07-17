from time import sleep

import nonebot
import requests

from qBot import api
from qBot.plugins import config


async def get_video():
    """
    获取视频url
    :return:
    """
    r = requests.get(api.VIDEO_URL)
    return r.text


def call_back_video(message_id):
    """
    通过异步撤回消息，不影响其他命令执行
    :param message_id:
    :return:
    """
    sleep(config.RECALL_TIME)
    nonebot.get_bot().delete_msg(message_id=message_id)
