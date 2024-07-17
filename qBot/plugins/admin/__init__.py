import asyncio
from time import sleep

from nonebot import on_command, CommandSession, permission

from qBot.plugins import config


@on_command('send_msg_in_groups', aliases=('群发', '通知'), permission=permission.SUPERUSER)
async def send_msg_in_groups(session: CommandSession):
    msg = session.current_arg_text.strip()
    if not msg:
        msg = (await session.aget(prompt='请输入需要群发的内容')).strip()
        if not msg:
            await msg.send('群发内容不能为空呢，请重新发起命令')
            return
    group_list = config.GROUP_LIST
    for group in group_list:
        try:
            await session.bot.send_group_msg(group_id=group, message=msg)
        except Exception as e:
            await session.send(f'群{group}发送失败，原因：{e}')
            continue
        await asyncio.sleep(2)
    await session.send('已经成功群发消息')
