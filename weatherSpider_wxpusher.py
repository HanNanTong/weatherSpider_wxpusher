import requests
from requests.exceptions import RequestException
import re

app_token = '#####'   # 本处改成自己的应用 APP_TOKEN
uid_myself = '#####'  # 本处改成自己的 UID

def wxpusher_send_by_webapi(msg):
    """利用 wxpusher 的 web api 发送 json 数据包，实现微信信息的发送"""
    webapi = 'http://wxpusher.zjiecode.com/api/send/message'
    data = {
        "appToken":app_token,
        "content":msg,
        "summary":msg[:99], # 该参数可选，默认为 msg 的前10个字符
        "contentType":1,
        "uids":[ uid_myself, ],
        }
    result = requests.post(url=webapi,json=data)
    return result.text

#获取一个页面内容
def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122 Safari / 537.36"
    }
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return response.status_code
    except RequestException:
        return "爬取失败！"
    
#解析获取的内容
def parse_one_page(html): 
    com = str( '.*?id="OverviewCurrentTemperature".*?target="_blank">(.*?)<span'    #气温
                + '.*?class="summaryCaptionCompact-E1_1">(.*?)</div>'               #天气
                + '.*?class="aqiColorCycle-E1_1">.*?</svg>(.*?)</div>')             #空气质量指数
    com1 = str('.*?<div class="lifeIndexItemContentV2-E1_1 textEllipsis-E1_1">(.*?)</div></div></a>')       #天气和生活：[驾车，户外运动，紫外线，感冒指数]
    
    pattern = re.compile(com, re.S)
    pattern1 = re.compile(com1, re.S)
    print('re解析中...')
    items = re.findall(pattern, html)
    items1 = re.findall(pattern1, html)
    print('re解析完毕，结果如下：')
    print(items)
    print(items1)
    print('--------------------------------------------------')

    
    print(items)
    dateList = []
    for item in items:
        dics = {
            '天气':item[1],
            '气温':int(item[0]),
            '空气质量指数':int(item[2]),
        }
        dateList.append(dics)

    dics = {
        '户外运动':items1[1],
        '紫外线指数':items1[2],
        '感冒指数':items1[3]
    }
    dateList.append(dics)
        
    return dateList


def push_msg(msg):
    result1 = wxpusher_send_by_webapi(msg)
    print(result1)

def main():
    url = '#####' # 修改为需要爬取的带位置的https://www.msn.cn/zh-cn/weather网址
    print('获取页面中...')
    html = get_one_page(url)
    print('页面获取成功！')
    #print(html)
    print('解析数据中...')
    weatherDate = parse_one_page(html)
    print('数据解析成功！')
    print(weatherDate)

    push_msg(str(weatherDate))

if __name__ == '__main__':
    main()

""" 
# 使用腾讯云函数调用时
def main_handler(event, context):   
    main()
 """