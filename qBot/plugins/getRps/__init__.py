from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession


@on_command('rps', aliases=('猜拳游戏', '猜拳'))
async def _(session: CommandSession):
    """
    猜拳游戏
    """
    msg = await session.send(MessageSegment.rps())
    a = await session.bot.get_msg(message_id=msg['message_id'])
    my_result = a['message'][0]['data']['result']
    user_result = (await session.aget(prompt='请出拳')).strip().replace('[CQ:rps,result=', '').replace(']', '')
    outcomes = {
        ('1', '1'): ('413', '啊哦，平局'),
        ('1', '2'): ('364', '恭喜，你赢了'),
        ('1', '3'): ('361', '你输了'),
        ('2', '1'): ('361', '你输了'),
        ('2', '2'): ('413', '啊哦，平局'),
        ('2', '3'): ('364', '恭喜，你赢了'),
        ('3', '1'): ('364', '恭喜，你赢了'),
        ('3', '2'): ('361', '你输了'),
        ('3', '3'): ('413', '啊哦，平局'),
    }

    face_id, outcome_msg = outcomes.get((my_result, user_result), ('413', '出现了一些错误'))

    await session.send(MessageSegment.face(int(face_id)) + outcome_msg)
