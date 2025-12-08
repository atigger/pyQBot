import time
from datetime import datetime

import requests
from qBot.plugins import config


async def get_fortune() -> str:
    """
    获取今日运势
    :return: 运势信息字符串
    """
    FORTUNE_URL = "https://m.weibo.cn/api/container/getIndex?type=uid&value=7230522444&containerid=1076037230522444"

    # 检查Cookie是否配置
    fortune_cookie = config.FORTUNE_COOKIE
    if not fortune_cookie or fortune_cookie.strip() == '':
        return "获取运势失败，Cookie未配置"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'Cookie': fortune_cookie,
        "Referer": "https://m.weibo.cn/u/7230522444"
    }
    try:
        r = requests.get(FORTUNE_URL, headers=headers, timeout=10)
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
                        if txt.find("公元") != -1:
                            if wbTime_day == current_day:
                                return "\n" + txt.replace("<br />", "\n")
        else:
            return "获取运势失败,网络连接失败"
    except Exception as e:
        print(e)
        return "获取运势失败,出现异常,详见控制台"
    return "获取运势失败,今日暂未发送运势"
