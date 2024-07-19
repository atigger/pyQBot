from nonebot import on_command, CommandSession

from qBot.plugins.getFortune.get_fortune import get_fortune


@on_command('fortune', aliases=('运势', '今日运势'))
async def _(session: CommandSession):
    """
    获取今日运势
    """
    fortune_txt = await get_fortune(False)
    await session.send(message=fortune_txt, at_sender=True)
