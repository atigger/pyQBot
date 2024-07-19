import asyncio

from aiocqhttp import MessageSegment
from nonebot import CommandSession, on_command

from qBot.plugins import config
from qBot.utils import delay_delete


async def create_message_node(user_id, images):
    nodes = []
    for image in images:
        node = {
            "type": "node",
            "data": {
                "name": "美女图片",
                "uin": user_id,
                "content": image
            }
        }
        nodes.append(node)
    return nodes


@on_command('beauty', aliases=('美女', '美女图片'))
async def _(session: CommandSession):
    """
    以合并转发的形式发送美女图片
    """
    tips_msg = await session.send("请耐心等待上传...")
    url = "https://img.0705.fun/mn.php?token=" + config.APP_ID
    images = [MessageSegment.image(url), MessageSegment.image(url),
              MessageSegment.image(url)]
    nodes = await create_message_node(123456, images)
    nodes_msg = await session.send(message=nodes)
    await session.bot.delete_msg(message_id=tips_msg['message_id'])
    message_id = nodes_msg['message_id']
    if config.RECALL_TIME != 0:
        asyncio.create_task(delay_delete(message_id, config.RECALL_TIME))
