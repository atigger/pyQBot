from aiocqhttp import Event
from nonebot import on_command, CommandSession, NLPSession, on_natural_language, IntentCommand

from qBot.plugins import config


@on_command('feed_back', aliases='反馈')
async def feed_back(session: CommandSession):
    """
    反馈
    """
    feed_back_txt = session.current_arg_text.strip()
    if not feed_back_txt:
        feed_back_txt = (await session.aget(prompt='请问你需要反馈什么问题?')).strip()
        if not feed_back_txt:
            await session.send('反馈问题不能为空呢，请重新发起命令')
            return
    feedback_nickname = session.ctx.sender['nickname']
    feed_back_msg = "用户:" + feedback_nickname + "(" + str(
        session.ctx.user_id) + ")\n反馈内容:" + feed_back_txt
    if session.ctx.message_type == 'group':
        group_name = await session.bot.get_group_info(group_id=session.ctx.group_id)
        group_name = group_name['group_name']
        feed_back_msg = feed_back_msg + "\n来自群:" + group_name + "(" + str(session.ctx.group_id) + ")"
    await session.bot.send_private_msg(user_id=config.SUPERUSERS, message=feed_back_msg)
    await session.send('反馈成功，感谢您的反馈！')


@on_natural_language(
    keywords={'反馈'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'feed_back')
