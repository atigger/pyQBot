from nonebot import on_command, CommandSession

from qBot.plugins.getPower.get_power import get_power


@on_command('power', aliases=('战力查询', '王者战力', '战力'))
async def _(session: CommandSession):
    """
    获取王者战力
    """
    hero_name = session.current_arg_text.strip()
    if not hero_name:
        hero_name = (await session.aget(prompt='请输入需要查询的王者英雄名')).strip()
        if not hero_name:
            await session.send('英雄名不能为空呢，请重新发起命令')
            return
    return await session.send(await get_power(hero_name))
