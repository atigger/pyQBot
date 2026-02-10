import os

import httpx
from nonebot import logger
from ruamel.yaml import YAML

from qBot import api, utils

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
VERSION = '1.3.5'
CONFIG_VERSION = '1.4'
yaml = YAML()


async def init_data():
    """
    初始化数据
    :return:
    """
    utils.mkdir(DATA_DIR)
    utils.mkdir(os.path.join(DATA_DIR, 'cache'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'qq'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'group'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'news'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'mofish'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'image'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'hero'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'voice'))
    utils.mkdir(os.path.join(DATA_DIR, 'cache', 'tarot'))
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


def read_config(key, key2=None, default=None):
    """
    读取某个配置项 如果读取失败 则返回默认值
    :param key: 键
    :param key2: 键2
    :param default: 默认值
    """
    try:
        config_data = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))
        if key2 is None:
            return config_data.get(key, default if default is not None else "")
        else:
            return config_data.get(key, {}).get(key2, default if default is not None else "")
    except:
        return default if default is not None else ""


async def update_config():
    """
    升级配置文件
    :return:
    """
    config_path = os.path.join(CONFIG_DIR, 'setting.yml')
    old_config = read_yaml_file(config_path)

    if str(old_config.get('Version', '')) == CONFIG_VERSION:
        return

    logger.info("升级配置文件")

    # 定义配置映射表，包含路径和默认值
    config_mapping = {
        'SuperUser': ([], ''),
        'ImageRecall': ([], 0),
        'AgreeFriend': ([], False),
        'AgreeGroup': ([], False),
        'NickName': ([], '机器人'),
        ('Auto', 'Group'): (['Auto'], []),
        ('Auto', 'AutoFortune'): (['Auto'], False),
        ('Auto', 'AutoNews'): (['Auto'], False),
        ('Auto', 'AutoTips'): (['Auto'], False),
        ('BaiDuAPI', 'APP_ID'): (['BaiDuAPI'], ''),
        ('BaiDuAPI', 'API_KEY'): (['BaiDuAPI'], ''),
        ('BaiDuAPI', 'SECRET_KEY'): (['BaiDuAPI'], ''),
        ('AI', 'Enable'): (['AI'], False),
        ('AI', 'ModelUrl'): (['AI'], ''),
        ('AI', 'ModelName'): (['AI'], ''),
        ('AI', 'Key'): (['AI'], ''),
        ('Notification', 'ApiUrl'): (['Notification'], ''),
        ('Notification', 'EnableBotMonitor'): (['Notification'], False),
        ('Fortune', 'Cookie'): (['Fortune'], '')
    }

    # 保存用户配置
    user_config = {}
    for key, (parent_keys, default_value) in config_mapping.items():
        if isinstance(key, tuple):
            # 嵌套配置
            parent_key, child_key = key
            value = old_config.get(parent_key, {}).get(child_key, default_value)
            if parent_key not in user_config:
                user_config[parent_key] = {}
            user_config[parent_key][child_key] = value
        else:
            # 顶级配置
            user_config[key] = old_config.get(key, default_value)

    # 删除旧配置文件并下载新的
    os.remove(config_path)
    await utils.downLoadFile(api.SETTING_URL, config_path)

    # 读取新配置模板并合并用户配置
    new_config = read_yaml_file(config_path)

    def deep_update(base_dict, update_dict):
        """递归更新字典"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    deep_update(new_config, user_config)

    # 强制更新Version为最新版本
    new_config['Version'] = CONFIG_VERSION

    # 写入更新后的配置文件
    with open(config_path, 'w', encoding="utf-8") as file:
        yaml.dump(new_config, file)


SUPERUSERS = read_config('SuperUser', default='')
RECALL_TIME = read_config('ImageRecall', default=0)
GROUP_LIST = read_config('Auto', 'Group', default=[])
ENABLE_AUTO_FORTUNE = read_config('Auto', 'AutoFortune', default=False)
ENABLE_AUTO_NEWS = read_config('Auto', 'AutoNews', default=False)
ENABLE_AUTO_TIPS = read_config('Auto', 'AutoTips', default=False)
APP_ID = read_config('BaiDuAPI', 'APP_ID', default='')
API_KEY = read_config('BaiDuAPI', 'API_KEY', default='')
SECRET_KEY = read_config('BaiDuAPI', 'SECRET_KEY', default='')
AGREE_FRIEND = read_config('AgreeFriend', default=False)
AGREE_GROUP = read_config('AgreeGroup', default=False)
AI_ENABLE = read_config('AI', 'Enable', default=False)
MODEL_URL = read_config("AI", 'ModelUrl', default='')
MODEL_NAME = read_config("AI", 'ModelName', default='')
AI_KEY = read_config("AI", 'Key', default='')
NICKNAME = read_config('NickName', default='机器人')
# 通知服务配置 - 添加判空和默认值处理
NOTIFICATION_API_URL = read_config('Notification', 'ApiUrl', default='')
ENABLE_BOT_MONITOR = read_config('Notification', 'EnableBotMonitor', default=False)
# 运势功能配置
FORTUNE_COOKIE = read_config('Fortune', 'Cookie', default='')
