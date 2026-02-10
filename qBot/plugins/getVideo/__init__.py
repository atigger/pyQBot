from aiocqhttp import MessageSegment
from nonebot import CommandSession, on_command, NLPSession, IntentCommand, on_natural_language

from qBot import api


@on_command('video', aliases='美女视频')
async def _(session: CommandSession):
    """
    获取美女视频
    """
    await session.send(MessageSegment.video(api.VIDEO_URL))


@on_natural_language(
    keywords={'美女视频'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'video')
