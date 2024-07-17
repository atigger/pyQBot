from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, IntentCommand

from qBot.plugins import config


@on_command('menu', aliases=('菜单', '帮助', "帮助文档"))
async def news(session: CommandSession):
    """
    获取菜单
    """
    msg = MessageSegment.face(147) + '           菜单          ' + MessageSegment.face(
        147) + '\n◇━━━━━━━━◇\n' + MessageSegment.face(
        333) + '今日运势(✔)  今日新闻(✔)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '星座运势(✔)  诸葛神签(✔)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '音乐系统(❌)  语音系统(❌)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '美女图片(❌)  美女视频(✔)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '战力查询(❌)  帮助文档(✔)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '喜报悲报(✔)  点赞名片(✔)' + MessageSegment.face(
        333) + '\n' + MessageSegment.face(333) + '猜拳游戏(✔)  骰子游戏(✔)' + MessageSegment.face(
        333) + '\n◇━━━━━━━━◇\nPS:@我并发相应文字查看指令\n发送@我反馈可反馈信息\n当前版本：' + config.VERSION
    await session.send(msg)


@on_natural_language(
    keywords={'菜单', '帮助', '帮助文档'})
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'menu')
