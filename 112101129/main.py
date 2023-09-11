from heapq import nlargest#取前n个值
import requests
import imageio.v2 as imageio# 图像处理
import jieba  # 中文分词
import urllib3#警告消除
import wordcloud  # 绘制词云
import time
from myclass.BLfunction import bilibili_search,re_send,save_data
from myclass.BLClass import bilibili
from threading import Thread
from threading import Lock
from queue import Queue

wait=Lock()

def BBC_Spider():
    while not bv_id.empty():
        video = bilibili()
        video.bvid = bv_id.get()  # 初始化bv号
        print("读取%s视频弹幕中..." % video.bvid)
        try:
            video.get_cid()  # 获取cid
            video.get_source()  # 获取弹幕内容
        except(requests.exceptions.ConnectionError, NameError):
            print("%s读取失败,准备重发..." % i)
            video = re_send(video)#重发
        if wait.acquire(True):#上锁防止冲突
            chat_list.extend(video.data)  # 将弹幕存到一个列表
            wait.release()#解锁
        time.sleep(1)#延迟等待

def video_search():
    while not n.empty():
        data=[]
        page=n.get()#获取页面
        while True:
            try:
                data=(bilibili_search(video.headers,int(page),"日本核污染水排海"))#返回列表
                break
            except(requests.exceptions.ConnectionError, NameError):
                print("第%d页读取失败，准备重发..."%i)
                continue#重发
        if wait.acquire(True):#上锁
            for j in data:
                bv_id.put(j) # 将列表写入队列
            wait.release()#解锁
    time.sleep(0.5)#延迟


urllib3.disable_warnings()#忽略警告
video=bilibili()#创建视频类
bv_id=Queue()#创建bv号存放列表
chat_list=[]#弹幕待写入列表
#获取综合排序前300的视频bv号并存放在bv_id列表

num=input("请输入要爬取的视频页数(一页20个视频)")
print("获取bv号中...")

n=Queue()
for i in range(int(num)):
    n.put(i+1)
threads_1=[]
for i in range(8):#8个线程
    t=Thread(target=video_search)#爬取搜索页
    threads_1.append(t)
    t.start()#开启线程
for i in threads_1:#等待线程结束
    i.join()

print("获取弹幕内容...")
threads_2=[]
for i in range(16):#16个线程
    t=Thread(target=BBC_Spider)#爬取弹幕
    threads_2.append(t)
    t.start()#开启线程

for i in threads_2:#等待线程结束
    i.join()

res_dic={}
for item in chat_list:#统计数量
    if item not in res_dic:
        res_dic[item]=1
    else:
        res_dic[item]+=1
res_sorted=sorted(res_dic.items(),key=lambda X:(X[1],X[0]),reverse=True)#按数量降序排序
save_data(res_sorted, r"./resource/bilibili_bullet_chat.csv")  # 写入文件夹


#输出数量前20个弹幕
print("弹幕数量前20列表")
max_list=nlargest(20, res_dic, key=lambda k: res_dic[k])#打印数量前20的弹幕
for i in max_list:
    print(i)

# file = open(r"resource/bilibili_bullet_chat.csv", encoding='utf-8')


txt = '\n'.join((chat_list))#合并
txt_list = jieba.lcut(txt)#分词
string = ' '.join((txt_list))#拼装

photo=imageio.imread(r'resource/核标志.png')#载入轮廓图
#设置词云图属性
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='C:/Windows/SIMLI.TTF',#字体
                        mask=photo,
                        scale=15,
                        stopwords={' '},
                        contour_width=5,
                        contour_color='black'
                        )
print("生成词云图中...")
w.generate(string)#生成词云图
w.to_file('resource/wordcloud.png')#存放文件








