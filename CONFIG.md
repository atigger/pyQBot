配置文件模板
```yaml
#配置文件版本
Version: 1.0
#管理员QQ
SuperUser: ""
#百度语音API
BaiDuAPI:
  APP_ID: ""
  API_KEY: ""
  SECRET_KEY: ""
#图片与视频自动撤回时间（0为不撤回,单位秒）(暂时禁用)
ImageRecall: 10
#自动同意好友请求
AgreeFriend: false
#自动同意邀请入群请求
AgreeGroup: false
#智能聊天开关
AI:
  Open: false
  Api_Key: ""
  Api_Secret: ""
#自动化操作
Auto:
  #自动发送运势信息
  AutoFortune: true
  #自动每日新闻信息
  AutoNews: true
  #自动发送摸鱼小提示
  AutoTips: true
  #需要自动发送的群列表 用,隔开
  Group: []
```
