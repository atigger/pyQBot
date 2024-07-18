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
                    wbTime_day = wbTime_datetime.day
                    current_weekday = time.localtime().tm_wday
                    current_day = time.localtime().tm_mday
                    txt = card['mblog']['text']
                    if wbTime_weekday == current_weekday:
                        if txt.find("播报") != -1:
                            f = open(config.DATA_DIR + "/cache/week.cache", "w")
                            f.write(str(current_weekday))
                            f.close()
                            if wbTime_day == current_day:
                                return "\n" + txt.replace("<br />", "\n")
        else:
            return "获取运势失败,网络连接失败"
    except Exception as e:
        print(e)
        return "获取运势失败,出现异常,详见控制台"
    return "获取运势失败,今日暂未发送运势"
