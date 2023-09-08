from heapq import nlargest#取前n个值
import requests
import imageio.v2 as imageio# 图像处理
import jieba  # 中文分词
import urllib3#警告消除
import wordcloud  # 绘制词云
from tqdm import tqdm#进度条
from myclass.BLfunction import bilibili_search,re_send,save_data
from myclass.BLClass import bilibili


urllib3.disable_warnings()#忽略警告
video=bilibili()#创建视频类
bv_id=[]#创建bv号存放列表
#获取综合排序前300的视频bv号并存放在bv_id列表
print("获取bv号中...")
num=input("请输入要爬取的视频页数(一页20个视频)")
for i in tqdm(range(int(num))):
    while True:
        try:
            bv_id.extend(bilibili_search(video.headers,i+1,"日本核污染水排海"))
            break
        except(requests.exceptions.ConnectionError, NameError):
            print("第%d页读取失败，准备重发..."%i)
            continue
print("获取弹幕内容...")
chat_list=[]
for i in tqdm(bv_id):
    video=bilibili()
    try:
        video.bvid=i#初始化bv号
        video.get_cid()#获取cid
        video.get_source()#获取弹幕内容
    except(requests.exceptions.ConnectionError,NameError):
        print("%s读取失败,准备重发..." % i)
        video=re_send(video)
    chat_list.extend(video.data)#将弹幕存到一个列表
save_data(chat_list, "resource/bilibili_bullet_chat.csv")  # 写入文件夹

#输出数量前20个弹幕
counter={}
for i in chat_list:#循环弹幕列表
    if i in counter.keys():
        counter[i] = counter[i]+1#如果存在相同弹幕，数量加1
    else:
        counter[i]=1#不存在相同弹幕，添加新弹幕
print(nlargest(20, counter, key=lambda k: counter[k]))#打印数量前20的弹幕

file = open('resource/bilibili_bullet_chat.csv', encoding='utf-8')

txt = file.read()
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
w.generate(string)#生成词云图
w.to_file('resource/wordcloud.png')#存放文件







