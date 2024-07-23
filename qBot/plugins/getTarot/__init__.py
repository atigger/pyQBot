from nonebot import on_command, CommandSession

from qBot.plugins.getTarot.get_tarot import get_tarot


@on_command('tarot', aliases=('抽塔罗牌', '塔罗牌'))
async def _(session: CommandSession):
    """
    抽塔罗牌
    """
    tips_msg = await session.send('正在祈祷中......')
    tarot_info = await get_tarot()
    await session.send(tarot_info)
    await session.bot.delete_msg(message_id=tips_msg['message_id'])
