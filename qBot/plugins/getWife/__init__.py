from nonebot import on_command, CommandSession

from qBot.plugins.getWife.get_wife import get_wife


@on_command('wife', aliases='抽老婆')
async def _(session: CommandSession):
    """
    抽老婆
    """
    tips_msg = await session.send('正在祈祷中......')
    tarot_info = await get_wife()
    await session.send(tarot_info)
    await session.bot.delete_msg(message_id=tips_msg['message_id'])
