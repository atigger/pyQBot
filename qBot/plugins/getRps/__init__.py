from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession


@on_command('rps', aliases=('猜拳游戏', '猜拳'))
async def rps(session: CommandSession):
    """
    猜拳游戏
    """
    msg = await session.send(MessageSegment.rps())
    a = await session.bot.get_msg(message_id=msg['message_id'])
    my_result: str = a['message'][0]['data']['result']
    user_result: str = (await session.aget(prompt='请出拳')).strip().replace('[CQ:rps,result=', '').replace(']', '')
    if my_result == '1':
        if user_result == '1':
            await session.send(MessageSegment.face(413))
            await session.send('啊哦，平局')
        elif user_result == '2':
            await session.send(MessageSegment.face(364))
            await session.send('恭喜，你赢了')
        elif user_result == '3':
            await session.send(MessageSegment.face(361))
            await session.send('你输了')
    elif my_result == '2':
        if user_result == '1':
            await session.send(MessageSegment.face(361))
            await session.send('你输了')
        elif user_result == '2':
            await session.send(MessageSegment.face(413))
            await session.send('啊哦，平局')
        elif user_result == '3':
            await session.send(MessageSegment.face(364))
            await session.send('恭喜，你赢了')
    elif my_result == '3':
        if user_result == '1':
            await session.send(MessageSegment.face(364))
            await session.send('恭喜，你赢了')
        elif user_result == '2':
            await session.send(MessageSegment.face(361))
            await session.send('你输了')
        elif user_result == '3':
            await session.send(MessageSegment.face(413))
            await session.send('啊哦，平局')
