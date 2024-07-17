import base64
import os.path
import time
import httpx
from nonebot import logger


def get_now_date():
    """
    获取当前日期
    格式：mmdd
    :return:
    """
    return time.strftime("%mm%dd", time.localtime())


async def downLoadFile(url, file_path):
    """
    下载文件
    :param url: 下载地址
    :param file_path: 保存路径
    :return True: 下载成功 False: 下载失败
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=30)
        with open(file_path, "wb") as f:
            f.write(r.content)
        logger.info("下载:" + os.path.basename(file_path) + "完成")
        if os.path.exists(file_path) is False:
            logger.info("下载失败")
            return False
        return True


def img_to_base64(img_path):
    """
    图片转base64
    :param img_path: 图片路径
    :return: base64字符串
    """
    with open(img_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read())
    return 'base64://' + image_base64.decode()


def mkdir(dir_path):
    """
    创建文件夹
    :param dir_path: 文件夹路径
    :return:
    """
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
