from nonebot import CommandSession, on_command, on_natural_language, NLPSession, IntentCommand

from qBot.plugins.getVoice.get_voice import get_voice


@on_command('voice', aliases='说')
async def _(session: CommandSession):
    """
    发送语音
    """
    txt = session.current_arg_text.strip()
    if not txt:
        txt = (await session.aget(prompt='请输入你想说的内容')).strip()
        if not txt:
            await session.send('内容不能为空呢，请重新发起命令')
            return
    await session.send(await get_voice(txt))


@on_natural_language(keywords={'说'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 判断消息是否以 '说' 开头，是则返回意图命令
    if stripped_msg.startswith('说'):
        args = stripped_msg.replace('说', '', 1)
        return IntentCommand(90.0, 'voice', current_arg=args)
    return IntentCommand(90.0, 'voice')
