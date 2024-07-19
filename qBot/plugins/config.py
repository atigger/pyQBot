import os

import httpx
import yaml

from qBot import api, utils

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
VERSION = '1.0.0'


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


def read_yaml_file(file_path):
    if os.path.exists(os.path.join(CONFIG_DIR, 'setting.yml')) is False:
        r = httpx.get(api.SETTING_URL)
        with open(os.path.join(CONFIG_DIR, 'setting.yml'), "wb") as f:
            f.write(r.content)
    with open(file_path, 'r', encoding="utf-8") as file:
        return yaml.safe_load(file)


SUPERUSERS = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['SuperUser']
RECALL_TIME = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['ImageRecall']
GROUP_LIST = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['Auto']['Group']
ENABLE_AUTO_FORTUNE = bool(read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['Auto']['AutoFortune'])
ENABLE_AUTO_NEWS = bool(read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['Auto']['AutoNews'])
ENABLE_AUTO_TIPS = bool(read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['Auto']['AutoTips'])
APP_ID = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['BaiDuAPI']['APP_ID']
API_KEY = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['BaiDuAPI']['API_KEY']
SECRET_KEY = read_yaml_file(os.path.join(CONFIG_DIR, 'setting.yml'))['BaiDuAPI']['SECRET_KEY']
