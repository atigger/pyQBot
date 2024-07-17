from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession


@on_command('dice', aliases=('骰子游戏', '色子游戏', '比大小'))
async def dice(session: CommandSession):
    """
    猜拳游戏
    """
    msg = await session.send(MessageSegment.dice())
    a = await session.bot.get_msg(message_id=msg['message_id'])
    my_result: str = a['message'][0]['data']['result']
    user_result: str = (await session.aget(prompt='请摇骰子')).strip().replace('[CQ:dice,result=', '').replace(']', '')
    if int(my_result) > int(user_result):
        await session.send(MessageSegment.face(361))
        await session.send('你输了')
    elif int(my_result) < int(user_result):
        await session.send(MessageSegment.face(364))
        await session.send('恭喜，你赢了')
    else:
        await session.send(MessageSegment.face(413))
        await session.send('啊哦，平局')
