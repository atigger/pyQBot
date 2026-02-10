import json
import os
import random

from qBot import utils
from qBot.plugins import config


async def get_sign(sender: str) -> str:
    """
    获取诸葛神签
    :param sender: 发送者
    :return 求签结果
    """
    try:
        f = open(os.path.join(config.DATA_DIR, 'cache', 'qq', sender + '.cache'), 'r', encoding='utf-8')
        json_txt = json.loads(f.read())
        if utils.get_now_date() != json_txt['date']:
            return get_sign_txt(sender)['sign']
        else:
            return json_txt['sign']
    except FileNotFoundError:
        return get_sign_txt(sender)['sign']


def get_sign_txt(sender):
    """
    设置诸葛神签
    :param sender: 发送者
    """
    f = open(os.path.join(config.DATA_DIR, '诸葛神签.txt'), 'r', encoding='utf-8')
    json_txt = {
        'date': utils.get_now_date(),
        'sign': random.choice(f.readlines()).replace('\n', '').replace("【", "\n【") + "\n【Tips】新增占卜功能，请发送占卜试试吧(*^_^*)"
    }
    f.close()
    f = open(os.path.join(config.DATA_DIR, 'cache', 'qq', sender + '.cache'), 'w', encoding='utf-8')
    f.write(json.dumps(json_txt))
    f.close()
    return json_txt
