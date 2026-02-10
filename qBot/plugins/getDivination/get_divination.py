from datetime import datetime

import requests
from qBot import api


async def get_divination():
    """
    获取诸葛神签
    返回格式化的占卜结果
    """
    try:
        response = requests.get(api.DIVINATION_URL, timeout=10)
        if response.status_code != 200:
            return "获取占卜结果失败，请稍后再试"

        data = response.json()

        # 结构化返回结果
        result = f"""\n
【卦名】{data.get('卦名', '未知')}
【卦文】{data.get('卦文', '未知')}
【卦意】{data.get('卦意', '未知')}
【卦级】{data.get('卦级', '未知')}

【签文】
{data.get('msg', '无签文')}

占卜时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()

        return result

    except requests.RequestException as e:
        return f"网络请求失败：{str(e)}"
    except KeyError as e:
        return f"数据解析错误：{str(e)}"
    except Exception as e:
        return f"获取占卜结果失败：{str(e)}"
