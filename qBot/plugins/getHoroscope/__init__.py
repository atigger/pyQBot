from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand
from qBot.plugins.getHoroscope.getHoroscope import get_horoscope

horoscope_mapping = {
    '白羊': 'aries',
    '金牛': 'taurus',
    '双子': 'gemini',
    '巨蟹': 'cancer',
    '狮子': 'leo',
    '处女': 'virgo',
    '天秤': 'libra',
    '天蝎': 'scorpio',
    '射手': 'sagittarius',
    '摩羯': 'capricorn',
    '水瓶': 'aquarius',
    '双鱼': 'pisces',
    '星座运势': '',
    '星座': '',
}


@on_command('horoscope', aliases=tuple(horoscope_mapping.keys()))
async def _(session: CommandSession):
    """
    获取星座运势
    """
    msg_txt = session.ctx.raw_message
    reply_txt = ""
    for chinese_name, english_name in horoscope_mapping.items():
        if chinese_name in msg_txt:
            if not english_name:
                reply_txt = "请@我并发送星座名\n例如 <@运势小助手 白羊>"
            else:
                reply_txt = await get_horoscope(english_name)
            break
    await session.send("\n" + reply_txt, at_sender=True)


@on_natural_language(keywords=set(horoscope_mapping.keys()))
async def _(session: NLPSession):
    return IntentCommand(90.0, 'horoscope')
