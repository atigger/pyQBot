import os

import requests
from aiocqhttp import MessageSegment, Message

from qBot import api, utils
from qBot.plugins import config


async def get_tarot() -> Message:
    """
    获取塔罗牌
    :return 塔罗牌结果
    """
    url = api.TAROT_URL
    response = requests.get(url)
    data = response.json()
    tarot_pic_path = os.path.join(config.DATA_DIR, 'cache', 'tarot', data['pic'] + ".png")
    if not os.path.exists(tarot_pic_path):
        await utils.downLoadFile(api.TAROT_IMG_URL + data['pic'] + '.png', tarot_pic_path)
    if data['position'] == "逆位":
        if not os.path.exists(os.path.join(config.DATA_DIR, 'cache', 'tarot', data['pic'] + '-逆位.png')):
            tarot_pic_path = await utils.turn_image(tarot_pic_path)
    msg = data['title'] + MessageSegment.image(utils.img_to_base64(tarot_pic_path)) + data['description']
    return msg
