import time
from datetime import datetime

import requests

from qBot.plugins import config


async def get_fortune() -> str:
    """
    获取今日运势
    """
    FORTUNE_URL = "https://m.weibo.cn/api/container/getIndex?type=uid&value=7230522444&containerid=1076037230522444"
    try:
        r = requests.get(FORTUNE_URL)
        if r.status_code == 200:
            data = r.json()
            if data['ok'] == 1:
                cards = data['data']['cards']
                for card in cards:
                    wbTime = card['mblog']['created_at']
                    wbTime_datetime = datetime.strptime(wbTime, "%a %b %d %H:%M:%S %z %Y")
                    wbTime_weekday = wbTime_datetime.weekday()
                    current_weekday = time.localtime().tm_wday
                    txt = card['mblog']['text']
                    if wbTime_weekday == current_weekday:
                        if txt.find("播报") != -1:
                            f = open(config.DATA_DIR + "/cache/week.cache", "w")
                            f.write(str(current_weekday))
                            f.close()
                            return "\n" + txt.replace("<br />", "\n")
        else:
            return "获取运势失败"
    except Exception as e:
        return "获取运势失败"
    return "获取运势失败"
