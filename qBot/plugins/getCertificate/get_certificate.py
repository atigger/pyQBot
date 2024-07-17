import random
import time

from qBot import api, untils
from qBot.plugins import config


async def get_good_news(msg):
    URL = api.PETPET_URL + "?key=certificate&textList=" + msg
    millis = int(round(time.time() * 1000))
    image_path = config.DATA_DIR + '\\cache\\image\\' + str(millis) + '.jpg'
    downLoad_tag = await untils.downLoadFile(URL, image_path)
    if downLoad_tag:
        return image_path
    else:
        return "生成喜报失败"


async def get_bad_news(msg):
    URL = api.PETPET_URL + "?key=sad_news&textList=" + msg
    millis = int(round(time.time() * 1000))
    image_path = config.DATA_DIR + '\\cache\\image\\' + str(millis) + '.jpg'
    downLoad_tag = await untils.downLoadFile(URL, image_path)
    if downLoad_tag:
        return image_path
    else:
        return "生成悲报失败"
