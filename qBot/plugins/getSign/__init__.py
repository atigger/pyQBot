from nonebot import on_command, CommandSession

from qBot.plugins.getSign.get_sign import get_sign


@on_command('sign', aliases=('求签', '诸葛神签'))
async def _(session: CommandSession):
    """
    获取诸葛神签
    """
    sign_txt = await get_sign(str(session.ctx.user_id))
    await session.send(message=sign_txt, at_sender=True)
