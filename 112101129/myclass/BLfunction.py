import csv
import time
from tqdm import tqdm
import requests
import json
from .BLClass import bilibili

#返回搜索页面的视频bv号列表
def bilibili_search(headers,page=1,keyword='test'):
    url="https://api.bilibili.com/x/web-interface/search/all/v2?page="+str(page)+"&keyword="+keyword
    r = requests.get(url, headers=headers, verify=False).text#返回json文本
    requests.get(url=url, params={'param': '1'}, headers={'Connection': 'close'})
    json_dick = json.loads(r)#将json文本转换为对象
    data=[]
    for i in range(20):#一个页面总计有20个视频
        data.append(json_dick['data']['result'][11]['data'][i]['bvid'])#将bv号添加进列表里
    time.sleep(0.2)
    return data

#将数据写入文件
def save_data(data,filename):
    with open(filename,"a",newline='',encoding='utf-8-sig') as file:# 打开文件
        writer=csv.writer(file)#对象初始化
        print("写入文件中...")
        for i in tqdm(data):#遍历列表
            t=[]
            t.append(i)
            writer.writerow(t)#用新列表使内容写入规范化
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