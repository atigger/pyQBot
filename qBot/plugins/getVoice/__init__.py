from nonebot import CommandSession, on_command

from qBot.plugins.getVoice.get_voice import get_voice


@on_command('voice', aliases='说')
async def _(session: CommandSession):
    """
    发送语音
    """
    txt = session.current_arg_text.strip()
    if not txt:
        hero_name = (await session.aget(prompt='请输入你想说的内容')).strip()
        if not hero_name:
            await session.send('内容不能为空呢，请重新发起命令')
            return
    await session.send(await get_voice(txt))
