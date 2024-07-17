from nonebot import on_command, CommandSession, logger


@on_command('like', aliases=('赞我', '点赞名片'))
async def send_like(session: CommandSession):
    try:
        await session.bot.send_like(user_id=session.ctx.user_id, times=10)
        msg = "点赞已完成"
    except Exception as e:
        if str(e).find("由于对方权限设置") != -1:
            msg = "点赞失败\n请检查设置->隐私->权限设置->允许陌生人点赞"
        elif str(e).find("今日同一好友点赞数已达上限") != -1:
            msg = "点赞失败，今日已达上限"
        else:
            msg = "点赞失败，未知错误" + str(e)
    await session.send(msg)
