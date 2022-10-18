# weatherSpider_wxpusher

# 爬取天气信息

**爬取带坐标信息的天气信息并使用wxpusher传递至手机微信进行提醒**

天气网页：https://www.msn.cn/zh-cn/weather/forecast/#####?loc=#####

wxpusher：[wxpusher](https://github.com/wxpusher/wxpusher-client)

---

**实现定时爬取可通过腾讯云函数**

如要实现每天8点、11点、16点运行一次即设置触发器中的corn表达式为 0 0 8,11,16 * * * * 。