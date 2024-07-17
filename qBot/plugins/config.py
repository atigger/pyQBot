import os

import httpx
import yaml

from qBot import api, untils

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
VERSION = '0.0.1'


async def init_data():
    """
    初始化数据
    :return:
    """
    untils.mkdir(DATA_DIR)
    untils.mkdir(DATA_DIR + '/cache')
    untils.mkdir(DATA_DIR + '/cache/qq')
    untils.mkdir(DATA_DIR + '/cache/group')
    untils.mkdir(DATA_DIR + '/cache/news')
    untils.mkdir(DATA_DIR + '/cache/mofish')
    untils.mkdir(DATA_DIR + '/cache/image')
    untils.mkdir(CONFIG_DIR)
    if os.path.exists(os.path.join(DATA_DIR, '诸葛神签.txt')) is False:
        await untils.downLoadFile(api.ZHU_GE_URL, os.path.join(DATA_DIR, '诸葛神签.txt'))
    if os.path.exists(os.path.join(CONFIG_DIR, 'setting.yml')) is False:
        await untils.downLoadFile(api.SETTING_URL, os.path.join(CONFIG_DIR, 'setting.yml'))


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
