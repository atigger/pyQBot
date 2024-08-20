配置文件模板
```yaml
#配置文件版本
Version: 1.3
#机器人昵称
NickName: ''
#管理员QQ
SuperUser: 0
#百度语音API
BaiDuAPI:
  APP_ID: ''
  API_KEY: ''
  SECRET_KEY: ''
#图片与视频自动撤回时间（0为不撤回,单位秒）(暂时禁用)
ImageRecall: 0
#自动同意好友请求
AgreeFriend: false
#自动同意邀请入群请求
AgreeGroup: false
#智能聊天开关
#Enable:是否启用AI功能
#ModelName:ollama模型名称或沫沫/婧枫
#ModelUrl:ollama模型地址 若使用沫沫/婧枫 此项可忽略
AI:
  Enable: false
  ModelName: ''
  ModelUrl: ''
  Key: ''
#自动化操作
Auto:
  #自动发送运势信息
  AutoFortune: false
  #自动每日新闻信息
  AutoNews: false
  #自动发送摸鱼小提示
  AutoTips: false
  #需要自动发送的群列表 用,隔开
  Group: []
```
