import asyncio

from aiocqhttp import MessageSegment
from nonebot import CommandSession, on_command, NLPSession, IntentCommand, on_natural_language

from qBot.plugins import config
from qBot.plugins.getVideo.get_video import get_video
from qBot.utils import delay_delete


@on_command('video', aliases='美女视频')
async def _(session: CommandSession):
    """
    获取美女视频
    """
    tips_msg = await session.send("正在祈祷中......")
    video_url = await get_video()
    video_msg = await session.send(MessageSegment.video(video_url))
    await session.bot.delete_msg(message_id=tips_msg['message_id'])
    message_id = video_msg['message_id']
    if config.RECALL_TIME != 0:
        asyncio.create_task(delay_delete(message_id, config.RECALL_TIME))


@on_natural_language(
    keywords={'美女视频'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'video')
