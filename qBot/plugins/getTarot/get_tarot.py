import os
import httpx
from aiocqhttp import MessageSegment

from qBot import api, utils
from qBot.plugins import config

error_msg = "啊偶，抽取失败了，请再试一次吧！"


async def get_tarot():
    """
    获取塔罗牌
    :return 塔罗牌结果
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api.TAROT_URL)
            response.raise_for_status()
        except httpx.RequestError:
            return error_msg

    data = response.json()
    tarot_pic_path = os.path.join(config.DATA_DIR, 'cache', 'tarot', f"{data['pic']}.png")

    if not os.path.exists(tarot_pic_path):
        if not await utils.downLoadFile(f"{api.TAROT_IMG_URL}{data['pic']}.png", tarot_pic_path):
            return error_msg

    if data['position'] == "逆位":
        ni_tarot_pic_path = os.path.join(config.DATA_DIR, 'cache', 'tarot', f"{data['pic']}-逆位.png")
        tarot_pic_path = await utils.turn_image(tarot_pic_path) if not os.path.exists(
            ni_tarot_pic_path) else ni_tarot_pic_path

    msg = data['title'] + MessageSegment.image(utils.img_to_base64(tarot_pic_path)) + data['description']
    return msg
