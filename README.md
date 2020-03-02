# pccold

**douyu斗鱼 自动化工具 主播上线通知 & 视频自动录制 & 弹幕抓取**

2020/3/3 by DKZ

## Install

use pip3

`$ sudo pip3 install pccold`

or download source code

`$ sudo python3 setup.py install`

## Usage

### 自动录像

`$ pccold`

后台运行
`$ nohup pccold &`

### 弹幕抓取

`$ pccolddanmu`

### 下载斗鱼视频

**旧功能未更新**

`$ pccoldvideo`

编辑下载列表
格式`[文件名](URL路径)`

`$ pccoldvideolist`

## Setting

`$ sudo vi /etc/pccold.conf`

```
room_id=20360 #斗鱼房间ID
stream_type="550p" #录像质量
is_cut=true #是否分段
how_long=1800 #录像分段长度(秒)
is_bypy=true #是否使用bypy上传百度云
is_bypy_rm=false #上传百度云后删除
download_path="/home/dkz/download" #录像保存路径
log_path="/home/dkz/pccold.log"
env="dev"

#录像配置
video_author="vJGdy0qrKwXy"
videolist_path="/home/dkz/videolist.md" #批量下载斗鱼视频列表

#邮件配置
my_email="recv@xx.com"
mail_sender="send@xx.com"
mail_passwd="xxx"
mail_host="xxx"
mail_port=25 #exmail.qq 465 or 25
pccold_contact="\n\npccold by DKZ \n---------------------\ngithub:https://github.com/davidkingzyb/pccold\n"
bypy_mail=true

#弹幕配置
username="visitor9986987" #弹幕登陆名
uid="1167614891" #弹幕 user ID
keyword="david,David" #记录关键词，以,分隔
keyuser="Pc冷冷" #关注用户名
keyuid="498062" #关注用户ID

```

## Reference

- python3
- [streamlink](https://github.com/streamlink/streamlink)
- [bypy](https://github.com/houtianze/bypy)
- [psutil](https://github.com/giampaolo/psutil)
- [websocket-clinet](https://github.com/websocket-client/websocket-client)
- [pystt](https://github.com/dust8/pystt)
- PyExecJS
- [real-url](https://github.com/wbt5/real-url/blob/master/douyu.py)








