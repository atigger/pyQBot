import asyncio

from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand, get_bot, logger

from qBot.plugins import config
from qBot.plugins.ollama.chat import ai_chat


@on_command('ollama')
async def _(session: CommandSession):
    message = session.state.get('message')
    message_id = session.ctx.message_id
    group_id = session.ctx.group_id
    user_id = session.ctx.user_id
    asyncio.create_task(ai(group_id, user_id, message_id, message))


async def ai(group_id: int, user_id: int, message_id: int, message: str):
    if group_id is None:
        think_msg = await get_bot().send_msg(message="正在思考,请稍等...", user_id=user_id)
        response = await ai_chat(message)  # 使用 await 等待异步函数完成
        await get_bot().send_msg(message=MessageSegment.reply(message_id) + response, user_id=user_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
    else:
        think_msg = await get_bot().send_group_msg(message="正在思考,请稍等...", group_id=group_id)
        response = await ai_chat(message)
        await get_bot().send_group_msg(message=MessageSegment.reply(message_id) + response, group_id=group_id)
        await get_bot().delete_msg(message_id=think_msg['message_id'])
        pass


@on_natural_language
async def _(session: NLPSession):
    if config.AI_ENABLE:
        if config.MODEL_URL != '' and config.MODEL_NAME != '':
            return IntentCommand(60.0, 'ollama', args={'message': session.msg_text})
        logger.error("未配置AI模型路径或名称")
    else:
        pass
