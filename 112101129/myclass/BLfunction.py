import time
import requests
import json
import openpyxl
from .BLClass import bilibili

#返回搜索页面的视频bv号列表

def bilibili_search(headers,page=1,keyword='test'):
    url="https://api.bilibili.com/x/web-interface/search/all/v2?page="+str(page)+"&keyword="+keyword
    r = requests.get(url, headers=headers, verify=False).text#返回json文本
    requests.get(url=url, params={'param': '1'}, headers={'Connection': 'close'})#关闭连接
    json_dick = json.loads(r)#将json文本转换为对象
    data=[]
    for i in range(20):#一个页面总计有20个视频
        data.append(json_dick['data']['result'][11]['data'][i]['bvid'])#将bv号添加进列表里
    time.sleep(0.2)
    return data

#将数据写入文件

def save_data(data,filename):
    workbook = openpyxl.Workbook()
    sh1 = workbook.create_sheet("sheet1")
    sh1.append(["弹幕内容", "数量"])
    for key, value in data:
        sh1.append([key, value])
    workbook.save('./resource/bilibili_bullet_chat.xlsx')
#重发

def re_send(video):
    while True:
        try:
            time.sleep(5)#延迟防检测
            video.get_source()  # 获取弹幕内容
            break
        except(requests.exceptions.ConnectionError, NameError):
            print("%s重发失败,再次重发..." % video.bvid)
            continue
    return video