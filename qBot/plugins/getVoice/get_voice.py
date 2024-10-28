import os
import time

from aiocqhttp import MessageSegment
from aip import AipSpeech

from qBot.plugins import config


async def get_voice(txt):
    """
    获取语音
    :param txt: 文本
    :return:
    """
    APP_ID = config.APP_ID
    API_KEY = config.API_KEY
    SECRET_KEY = config.SECRET_KEY
    if APP_ID == "" or API_KEY == "" or SECRET_KEY == "":
        return "百度API未配置"
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    client.setConnectionTimeoutInMillis(2000)
    client.setSocketTimeoutInMillis(60000)
    result = client.synthesis(txt, "zh", 1)
    if not isinstance(result, dict):
        mp3_path = os.path.join(config.DATA_DIR, 'cache', 'voice', str(int(round(time.time() * 1000))) + '.mp3')
        with open(mp3_path, 'wb') as f:
            f.write(result)
        return MessageSegment.record(mp3_path)
