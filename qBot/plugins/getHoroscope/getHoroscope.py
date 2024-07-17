import requests

from qBot import api


async def get_horoscope(keywords):
    """
    获取星座运势
    :param keywords: 星座
    """
    URL = api.HOROSCOPE_URL + "?type=" + keywords + "&time=today"
    try:
        response = requests.get(URL)
        if response.status_code != 200:
            return "获取星座运势失败"
        else:
            data = response.json()["data"]
        title = data["title"] + data["type"] + "\n"
        todo = "宜:" + data["todo"]["yi"] + "\n忌:" + data["todo"]["ji"] + "\n"
        fortune = "总运势:" + data["index"]["all"] + "\n" + data["fortunetext"]["all"] + "\n" + \
                  "爱情运势:" + data["index"]["love"] + "\n" + data["fortunetext"]["love"] + "\n" + \
                  "财富运势:" + data["index"]["money"] + "\n" + data["fortunetext"]["money"] + "\n" + \
                  "工作运势:" + data["index"]["work"] + "\n" + data["fortunetext"]["work"] + "\n" + \
                  "健康运势:" + data["index"]["health"] + "\n" + data["fortunetext"]["health"] + "\n"
        lucky_number = "幸运数字:" + data["luckynumber"] + "\n"
        lucky_color = "幸运颜色:" + data["luckycolor"] + "\n"
        short_comment = "短评:" + data["shortcomment"]
        return title + todo + lucky_number + lucky_color + todo + fortune + short_comment
    except Exception as e:
        return "获取星座运势失败"
