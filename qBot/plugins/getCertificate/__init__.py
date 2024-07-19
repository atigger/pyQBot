from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession, NLPSession, on_natural_language, IntentCommand

from qBot import api


@on_command('good_news', aliases='喜报')
async def _(session: CommandSession):
    """
    获取喜报
    """
    msg = session.current_arg_text.strip()
    if not msg:
        msg = (await session.aget(prompt='请输入喜报内容')).strip()
        if not msg:
            await session.send('喜报内容不能为空呢，请重新发起命令')
            return
    msg_id = await session.send(message="正在生成,请耐心等待...")
    img_url = api.PETPET_URL + "?key=certificate&textList=" + msg
    try:
        await session.send(MessageSegment.image(img_url))
    except:
        await session.send(MessageSegment.image("生成喜报失败"))
    await session.bot.delete_msg(message_id=msg_id['message_id'])


@on_command('bad_news', aliases='悲报')
async def _(session: CommandSession):
    """
    获取悲报
    """
    msg = session.current_arg_text.strip()
    if not msg:
        msg = (await session.aget(prompt='请输入悲报内容')).strip()
        if not msg:
            await session.send('悲报内容不能为空呢，请重新发起命令')
            return
    msg_id = await session.send(message="正在生成,请耐心等待...")
    img_url = api.PETPET_URL + "?key=sad_news&textList=" + msg
    try:
        await session.send(MessageSegment.image(img_url))
    except:
        await session.send(MessageSegment.image("生成悲报失败"))
    await session.bot.delete_msg(message_id=msg_id['message_id'])


@on_natural_language(keywords={'喜报', '悲报'})
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 判断消息是否以 '喜报' 或 '悲报' 开头，是则返回意图命令
    if stripped_msg.find('喜报悲报') != -1:
        await session.send('请以以下格式输入\n喜报 喜报内容\n悲报 悲报内容')
        return
    if stripped_msg.startswith('喜报'):
        args = stripped_msg.replace('喜报', '')
        return IntentCommand(90.0, 'good_news', current_arg=args)
    elif stripped_msg.startswith('悲报'):
        args = stripped_msg.replace('悲报', '')
        return IntentCommand(90.0, 'bad_news', current_arg=args)
