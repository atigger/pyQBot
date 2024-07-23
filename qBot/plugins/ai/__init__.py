import asyncio

from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand, get_bot, logger

from qBot.plugins import config
from qBot.plugins.ai.chat import ollama_ai, lolimi_ai


@on_command('ollama')
async def _(session: CommandSession):
    message = session.state.get('message')
    message_id = session.ctx.message_id
    group_id = session.ctx.group_id
    user_id = session.ctx.user_id
    asyncio.create_task(ollama_ai(group_id, user_id, message_id, message))


@on_command('lolimi')
async def _(session: CommandSession):
    message = session.state.get('message')
    message_id = session.ctx.message_id
    group_id = session.ctx.group_id
    user_id = session.ctx.user_id
    asyncio.create_task(lolimi_ai(group_id, user_id, message_id, message))


@on_natural_language
async def _(session: NLPSession):
    if config.AI_ENABLE:
        if config.MODEL_NAME == "沫沫" or config.MODEL_NAME == "婧枫":
            return IntentCommand(60.0, 'lolimi', args={'message': session.msg_text})
        if config.MODEL_URL != '' and config.MODEL_NAME != '':
            return IntentCommand(60.0, 'ollama', args={'message': session.msg_text})
        logger.error("未配置AI模型路径或名称")
    else:
        pass
