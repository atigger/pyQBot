from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession


@on_command('dice', aliases=('骰子游戏', '色子游戏', '比大小'))
async def _(session: CommandSession):
    """
    骰子游戏
    """
    msg = await session.send(MessageSegment.dice())
    msg_id = await session.bot.get_msg(message_id=msg['message_id'])
    bot_result = int(msg_id['message'][0]['data']['result'])
    user_result = int((await session.aget(prompt='请摇骰子')).strip().replace('[CQ:dice,result=', '').replace(']', ''))
    outcomes = {
        bot_result > user_result: (361, '你输了'),
        bot_result < user_result: (364, '恭喜，你赢了'),
        bot_result == user_result: (413, '啊哦，平局')
    }

    face_id, outcome_msg = outcomes[True]
    await session.send(MessageSegment.face(face_id) + outcome_msg)
