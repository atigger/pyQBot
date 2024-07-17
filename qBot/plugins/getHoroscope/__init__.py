from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand

from qBot.plugins.getHoroscope.getHoroscope import get_horoscope


@on_command('horoscope', aliases=(
        '星座运势', '星座', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶',
        '双鱼'))
async def getHoroscope(session: CommandSession):
    msg_txt = session.ctx.raw_message
    reply_txt = "\n请@我并发送星座名\n例如 <@运势小助手 白羊>"
    if msg_txt.find('白羊') != -1:
        reply_txt = await get_horoscope('aries')
    elif msg_txt.find('金牛') != -1:
        reply_txt = await get_horoscope('taurus')
    elif msg_txt.find('双子') != -1:
        reply_txt = await get_horoscope('gemini')
    elif msg_txt.find('巨蟹') != -1:
        reply_txt = await get_horoscope('cancer')
    elif msg_txt.find('狮子') != -1:
        reply_txt = await get_horoscope('leo')
    elif msg_txt.find('处女') != -1:
        reply_txt = await get_horoscope('virgo')
    elif msg_txt.find('天秤') != -1:
        reply_txt = await get_horoscope('libra')
    elif msg_txt.find('天蝎') != -1:
        reply_txt = await get_horoscope('scorpio')
    elif msg_txt.find('射手') != -1:
        reply_txt = await get_horoscope('sagittarius')
    elif msg_txt.find('摩羯') != -1:
        reply_txt = await get_horoscope('capricorn')
    elif msg_txt.find('水瓶') != -1:
        reply_txt = await get_horoscope('aquarius')
    elif msg_txt.find('双鱼') != -1:
        reply_txt = await get_horoscope('pisces')
    await session.send("\n" + reply_txt, at_sender=True)


@on_natural_language(
    keywords={'白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '摩羯', '水瓶', '双鱼'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'horoscope')
