import requests
from aiocqhttp import MessageSegment

from qBot import api


async def get_wife():
    """
    抽老婆
    :return 结果
    """
    url = api.WIFE_URL
    response = requests.get(url)
    data = response.json()
    return "今天的二次元老婆是~【" + data['wife'].split(".")[0] + "】哒" + MessageSegment.image(
        api.WIFE_IMG_URL + data['wife'])
