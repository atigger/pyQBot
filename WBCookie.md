## 微博Cookie获取
要使用今日运势查询功能，需要获取新浪微博的Cookie。以下是获取Cookie的步骤：
1. 打开浏览器，访问[新浪微博网站](https://m.weibo.cn/u/7230522444)。
2. 登录后，按下`F12`键打开开发者工具。
3. 在开发者工具中，选择`Network`（网络）选项卡。
4. 刷新页面，然后在网络请求列表中找到 https://m.weibo.cn/api/container/getIndex?type=uid&value=xxxx&containerid=xxx 的请求。
5. 点击该请求，查看其详细信息，找到`Headers`（请求头）部分。
6. 在请求头中，找到`Cookie`字段，复制其内容。
