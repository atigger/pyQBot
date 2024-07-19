from nonebot import on_command, CommandSession

from qBot.plugins.getMusic.getMusic import get_music


@on_command('music', aliases=('听歌', '点歌', '音乐系统'))
async def _(session: CommandSession):
    music_name = session.current_arg_text.strip()
    if not music_name:
        music_name = (await session.aget(prompt='请输入歌曲名')).strip()
        if not music_name:
            await session.send('歌曲名不能为空呢，请重新发起命令')
            return
    await session.send(get_music(music_name))
