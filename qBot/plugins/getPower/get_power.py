import os
import requests
from aiocqhttp import MessageSegment
from qBot import utils, api
from qBot.plugins import config
from qBot.utils import downLoadFile


async def get_power(hero_name):
    if not hero_name:
        return "请输入英雄名称"

    hero_info = {
        "alias_name": "",
        "photo": "",
        "qq": {"province": "", "province_power": "", "city": "", "city_power": "", "area": "", "area_power": "",
               "guobiao": ""},
        "wx": {"province": "", "province_power": "", "city": "", "city_power": "", "area": "", "area_power": "",
               "guobiao": ""}
    }

    for platform in ["qq", "wx"]:
        url = api.HERO_POWER_URL + "?hero=" + hero_name + "&type=" + platform
        try:
            response = requests.get(url)
            data = response.json()["data"]
            hero_info["alias_name"] = data["name"]
            hero_info["photo"] = data["photo"]
            hero_info[platform] = {
                "province": data["province"],
                "province_power": data["provincePower"],
                "city": data["city"],
                "city_power": data["cityPower"],
                "area": data["area"],
                "area_power": data["areaPower"],
                "guobiao": data["guobiao"]
            }
        except Exception as e:
            print(e)

    if hero_info["alias_name"]:
        file_path = os.path.join(config.DATA_DIR, 'cache', 'hero', hero_info["alias_name"] + '.jpg')
        if not os.path.exists(file_path):
            await downLoadFile(hero_info["photo"], file_path)

        return MessageSegment.image(utils.img_to_base64(file_path)) + "\n" + \
            f"【{hero_info['alias_name']}】\n" + \
            "QQ战力：\n" + \
            f"{hero_info['qq']['province']}：{hero_info['qq']['province_power']}\n" + \
            f"{hero_info['qq']['city']}：{hero_info['qq']['city_power']}\n" + \
            f"{hero_info['qq']['area']}：{hero_info['qq']['area_power']}\n" + \
            f"QQ国标：{hero_info['qq']['guobiao']}\n" + \
            "微信战力：\n" + \
            f"{hero_info['wx']['province']}：{hero_info['wx']['province_power']}\n" + \
            f"{hero_info['wx']['city']}：{hero_info['wx']['city_power']}\n" + \
            f"{hero_info['wx']['area']}：{hero_info['wx']['area_power']}\n" + \
            f"微信国标：{hero_info['wx']['guobiao']}"
    else:
        return "未找到该英雄,请尝试输入英雄全称"
