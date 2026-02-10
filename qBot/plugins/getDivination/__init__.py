from nonebot import on_command, CommandSession
from .get_divination import get_divination


@on_command('divination', aliases=('占卜', '摇卦占卜', '摇卦'))
async def _(session: CommandSession):
    """
    获取占卜结果
    """
    divination_txt = await get_divination()
    await session.send(message=divination_txt, at_sender=True)
