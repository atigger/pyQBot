import os

import httpx
from nonebot import logger
from ruamel.yaml import YAML

from qBot import api, utils

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
VERSION = '1.1.0'
CONFIG_VERSION = '1.1'
yaml = YAML()


async def init_data():
    """
    初始化数据
    :return:
    """
    utils.mkdir(DATA_DIR)
    utils.mkdir(DATA_DIR + '/cache')
    utils.mkdir(DATA_DIR + '/cache/qq')
    utils.mkdir(DATA_DIR + '/cache/group')
    utils.mkdir(DATA_DIR + '/cache/news')
    utils.mkdir(DATA_DIR + '/cache/mofish')
    utils.mkdir(DATA_DIR + '/cache/image')
    utils.mkdir(DATA_DIR + '/cache/hero')
    utils.mkdir(DATA_DIR + '/cache/voice')
    utils.mkdir(CONFIG_DIR)
    if os.path.exists(os.path.join(DATA_DIR, '诸葛神签.txt')) is False:
        await utils.downLoadFile(api.ZHU_GE_URL, os.path.join(DATA_DIR, '诸葛神签.txt'))
    if os.path.exists(os.path.join(CONFIG_DIR, 'setting.yml')) is False:
        await utils.downLoadFile(api.SETTING_URL, os.path.join(CONFIG_DIR, 'setting.yml'))
    else:
        await update_config()


def read_yaml_file(file_path):
    """
    读取yaml文件
    :param file_path: 文件路径
    :return: 文件内容
    """
    if not os.path.exists(file_path):
        r = httpx.get(api.SETTING_URL)
        with open(file_path, "wb") as f:
            f.write(r.content)
    with open(file_path, 'r', encoding="utf-8") as file:
        return yaml.load(file)


def read_config(key, key2=None):
    """
    读取某个配置项 如果读取失败 则返回空
    :param key: 键
    :param key2: 键2
    """
    try:
        if key2 is None:
            return read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))[key]
        else:
            return read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))[key][key2]
    except:
        return ""


async def update_config():
    """
    升级配置文件
    :return:
    """
    config_path = os.path.join(CONFIG_DIR, 'setting.yml')
    config_data = read_yaml_file(config_path)
    if config_data['Version'] == CONFIG_VERSION:
        return
    logger.info("升级配置文件")
    # 读取老配置项
    SUPERUSERS1 = read_config('SuperUser')
    RECALL_TIME1 = read_config('ImageRecall')
    GROUP_LIST1 = read_config('Auto', 'Group')
    ENABLE_AUTO_FORTUNE1 = read_config('Auto', 'AutoFortune')
    ENABLE_AUTO_NEWS1 = read_config('Auto', 'AutoNews')
    ENABLE_AUTO_TIPS1 = read_config('Auto', 'AutoTips')
    APP_ID1 = read_config('BaiDuAPI', 'APP_ID')
    API_KEY1 = read_config('BaiDuAPI', 'API_KEY')
    SECRET_KEY1 = read_config('BaiDuAPI', 'SECRET_KEY')
    AGREE_FRIEND1 = read_config('AgreeFriend')
    AGREE_GROUP1 = read_config('AgreeGroup')
    # 删除之前的配置文件
    os.remove(config_path)
    # 更新配置文件
    await utils.downLoadFile(api.SETTING_URL, config_path)
    # 写入配置文件
    config_data = read_yaml_file(config_path)
    config_data['SuperUser'] = SUPERUSERS1
    config_data['ImageRecall'] = RECALL_TIME1
    config_data['Auto']['Group'] = GROUP_LIST1
    config_data['Auto']['AutoFortune'] = ENABLE_AUTO_FORTUNE1
    config_data['Auto']['AutoNews'] = ENABLE_AUTO_NEWS1
    config_data['Auto']['AutoTips'] = ENABLE_AUTO_TIPS1
    config_data['BaiDuAPI']['APP_ID'] = APP_ID1
    config_data['BaiDuAPI']['API_KEY'] = API_KEY1
    config_data['BaiDuAPI']['SECRET_KEY'] = SECRET_KEY1
    config_data['AgreeFriend'] = AGREE_FRIEND1
    config_data['AgreeGroup'] = AGREE_GROUP1
    with open(config_path, 'w', encoding="utf-8") as file:
        yaml.dump(config_data, file)


SUPERUSERS = read_config('SuperUser')
RECALL_TIME = read_config('ImageRecall')
GROUP_LIST = read_config('Auto', 'Group')
ENABLE_AUTO_FORTUNE = read_config('Auto', 'AutoFortune')
ENABLE_AUTO_NEWS = read_config('Auto', 'AutoNews')
ENABLE_AUTO_TIPS = read_config('Auto', 'AutoTips')
APP_ID = read_config('BaiDuAPI', 'APP_ID')
API_KEY = read_config('BaiDuAPI', 'API_KEY')
SECRET_KEY = read_config('BaiDuAPI', 'SECRET_KEY')
AGREE_FRIEND = read_config('AgreeFriend')
AGREE_GROUP = read_config('AgreeGroup')
AI_ENABLE = read_config('AI', 'Enable')
MODEL_URL = read_config("AI", 'ModelUrl')
MODEL_NAME = read_config("AI", 'ModelName')
