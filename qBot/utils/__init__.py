import asyncio
import base64
import os.path
import time
from PIL import Image
import httpx
from nonebot import logger, get_bot

from qBot import api


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


async def generate_picture_url(key: str, text: str, type: str):
    """
    生成图片
    :param key: 键
    :param text: 文本
    :param type: 类型
    """
    URL = ""
    if type == "txt":
        URL = api.PETPET_URL + "?key=" + key + "&textList=" + text
    elif type == "img" or type == "gif":
        URL = api.PETPET_URL + "?key=" + key + "&toAvatar=" + text
    return URL


async def delay_delete(message_id, wait_time):
    """
    等待撤回消息
    :param message_id: 消息ID
    :param wait_time: 等待时间
    """
    await asyncio.sleep(wait_time)
    await get_bot().delete_msg(message_id=message_id)  # 撤回消息


async def turn_image(image_path):
    """
    图片旋转
    :param image_path: 图片路径
    :return: 旋转后的图片路径
    """
    # Load the image
    image = Image.open(image_path)

    # Rotate the image by 180 degrees
    rotated_image = image.rotate(180)

    # Split the path to extract directory, filename, and extension
    dir_name, file_name = os.path.split(image_path)
    file_root, file_ext = os.path.splitext(file_name)

    # Append the suffix "-逆位" to the filename
    new_file_name = f"{file_root}-逆位{file_ext}"

    # Combine to form the new path
    new_image_path = os.path.join(dir_name, new_file_name)

    # Save the rotated image to the new path
    rotated_image.save(new_image_path)

    return new_image_path
