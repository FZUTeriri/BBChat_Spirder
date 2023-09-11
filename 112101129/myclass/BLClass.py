import time
import requests
import json
import re
class bilibili:
    def __init__(self,bvid='BV17x411w7KC'):
        self.bvid=bvid#bv号
        self.data=[]#弹幕内容
        self.cid='0'#视频cid号
        self.headers={'user-angent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
              'cookie':"buvid3=9A6C4A71-232F-424F-9956-DE5AE542662F167618infoc; LIVE_BUVID=AUTO9216323908811475; CURRENT_BLACKGAP=0; blackside_state=0; buvid_fp_plain=undefined; DedeUserID=76795189; DedeUserID__ckMd5=5a6b22515ce847ed; buvid4=BFC8C35B-2216-2D9C-2559-EF1372F54A7058821-022012116-YqP%2BXrgApe6oAVU0obWpwA%3D%3D; b_nut=100; balh_server_inner=__custom__; balh_is_closed=; ogv_channel_version=v1; i-wanna-go-back=-1; b_ut=5; is-2022-channel=1; _uuid=D78105518-938B-64AF-7965-875821BE3C8248895infoc; fingerprint3=80bbd1cd670cc933fb2ccc344f534a95; rpdid=|(u))kkYu|kk0J'uYY)Ymuukk; balh_server_custom_tw=https://api.qiu.moe; balh_generate_sub=Y; balh_mode=default; balh_server_custom_cn=; balh_server_custom_hk=https://unlock-bilibili-bilibili-unlock-heavxfgbhu.cn-hongkong.fcapp.run; nostalgia_conf=-1; CURRENT_PID=dfeb8dd0-c887-11ed-a27d-af5ff8c1d057; balh_server_custom=https://unlock-bilibili-bilibili-unlock-heavxfgbhu.cn-hongkong.fcapp.run; hit-dyn-v2=1; CURRENT_FNVAL=4048; FEED_LIVE_VERSION=V8; home_feed_column=5; browser_resolution=1536-754; hit-new-style-dyn=1; CURRENT_QUALITY=116; fingerprint=7d299747b862c8d7bf5b0c1d881f9128; header_theme_version=CLOSE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTM5MjcxNTUsImlhdCI6MTY5MzY2Nzk1NSwicGx0IjotMX0.JMm8Qmb8xxd-EA8UQEmMH9XOkrijinzt0t7b7wEMnAc; bili_ticket_expires=1693927155; bp_t_offset_76795189=837481260807880774; bsource=search_bing; buvid_fp=7d299747b862c8d7bf5b0c1d881f9128; PVID=11; b_lsid=19B61087F_18A645E78DB; SESSDATA=9b09be5e%2C1709453039%2Cd6cfe%2A92HTzqSNOFfGXcI4uK4CIJWRbeKiblp3_k-QNY55i3jR3D8xtLwvDhEvqnCVI7NNUftzYfoQAAWQA; bili_jct=ba91050e3fa16314989f5d560ba795fa; sid=g670pf3m"
              }#请求头

    #获取cid

    def get_cid(self):
        url="https://api.bilibili.com/x/player/pagelist?bvid="+self.bvid
        res=requests.get(url,self.headers).text#放回json文本
        requests.get(url=url, params={'param': '1'}, headers={'Connection': 'close'})#关闭连接
        res_json=json.loads(res)#将jons文本转换为对象
        self.cid=res_json['data'][0]['cid']#读取cid
        time.sleep(0.1)

    #获取弹幕内容

    def get_source(self):
        url="https://comment.bilibili.com/"+str(self.cid)+".xml"
        response=requests.get(url,self.headers)#返回xml文件
        requests.get(url=url, params={'param': '1'}, headers={'Connection': 'close'})#关闭连接
        res_doc=response.content.decode('utf-8')
        res=re.compile('<d.*?>(.*?)</d>')#正则匹配
        self.data=re.findall(res,res_doc)#将内容写入列表
        time.sleep(0.1)

