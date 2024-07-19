import requests
from aiocqhttp import MessageSegment


def get_music(music_name):
    url = 'https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg'
    params = {
        "format": "json",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "notice": 0,
        "platform": "yqq.json",
        "needNewCode": 0,
        "uin": 0,
        "hostUin": 0,
        "is_xml": 0,
        "key": music_name,
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        song_id = r.json()['data']['song']['itemlist'][0]['id']
        msg: MessageSegment = MessageSegment.music("qq", int(song_id))
        return msg
    return MessageSegment.text("QQ音乐中找不到相关的歌曲")
