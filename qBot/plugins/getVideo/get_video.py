import requests

from qBot import api


async def get_video():
    """
    获取视频url
    :return:
    """
    r = requests.get(api.VIDEO_URL)
    return r.text
