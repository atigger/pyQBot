import httpx
import ollama
from aiocqhttp import MessageSegment
from nonebot import get_bot

from qBot import api
from qBot.plugins import config

bot_name = config.NICKNAME


async def ollama_ai(group_id: int, user_id: int, message_id: int, message: str):
    if group_id is None:
        think_msg = await get_bot().send_msg(message=bot_name + "正在思考中,请稍等...", user_id=user_id)
        response = await ai_chat(message)  # 使用 await 等待异步函数完成
        await get_bot().send_msg(message=MessageSegment.reply(message_id) + response, user_id=user_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
    else:
        think_msg = await get_bot().send_group_msg(message=bot_name + "正在思考中,请稍等...", group_id=group_id)
        response = await ai_chat(message)
        await get_bot().send_group_msg(message=MessageSegment.reply(message_id) + response, group_id=group_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
        pass


async def lolimi_ai(group_id: int, user_id: int, message_id: int, message: str):
    if config.MODEL_NAME == "沫沫":
        url = api.MomoURL + message
    else:
        url = api.JingfengURL + message
    if group_id is None:
        think_msg = await get_bot().send_msg(message=bot_name + "正在思考中" + MessageSegment.face(355),
                                             user_id=user_id)
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=60)
                response = r.json()
            reply_msg = response['data']['output'].replace("沫沫", bot_name).replace("婧枫", bot_name)
        except:
            reply_msg = "网络太拥挤," + bot_name + "已经坏掉啦，请稍后再试" + MessageSegment.face(354)
        await get_bot().send_msg(message=MessageSegment.reply(message_id) + reply_msg, user_id=user_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
    else:
        think_msg = await get_bot().send_group_msg(message=bot_name + "正在思考中" + MessageSegment.face(355),
                                                   group_id=group_id)
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=60)
                response = r.json()
            reply_msg = response['data']['output'].replace("沫沫", bot_name).replace("婧枫", bot_name)
        except:
            reply_msg = "网络太拥挤," + bot_name + "已经坏掉啦，请稍后再试" + MessageSegment.face(354)
        await get_bot().send_group_msg(message=MessageSegment.reply(message_id) + reply_msg, group_id=group_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
        pass


async def ai_chat(msg: str):
    client = ollama.AsyncClient(host=config.MODEL_URL)
    message = ""
    messages = [
        {
            'role': 'user',
            'content': msg,
        },
    ]
    async for response in await client.chat(model=config.MODEL_NAME, messages=messages, stream=True):
        if response['done']:  # 如果响应表示聊天结束
            return message
        message = message + response['message']['content']  # 获取响应消息
        pass
