# pccold

**douyu斗鱼 自动化工具 主播上线通知 & 视频自动录制 & 弹幕抓取 & 下载斗鱼视频**

2018/10/5 by DKZ




## Dependence

- python3
- [streamlink](https://github.com/streamlink/streamlink)
- [bypy](https://github.com/houtianze/bypy)

## Config

当前目录下新建conf.py

```
room_id="cold" #斗鱼房间ID
room_num=20360 #斗鱼房间数字ID
stream_type='medium' #录像质量 source|medium|low
is_cut=True #是否分段
how_long=60*30 #录像分段长度(秒)
is_bypy=True #是否使用bypy上传百度云
download_path="./download" #录像保存路径
videolist_path='videolist.md' #批量下载斗鱼视频列表

#api
room_api='http://open.douyucdn.cn/api/RoomApi/room/' 
room_url="http://www.douyutv.com/"

#邮件配置
my_email="recv@xx.com"
mail_sender='send@xx.com'
mail_passwd='xxx'
mail_host='xxx'
mail_port=25 #exmail.qq 465 or 25
pccold_contact="\n\npccold by DKZ \n---------------------\ngithub:https://github.com/davidkingzyb/pccold\ncontact:davidkingzyb@qq.com  @__DKZ__\naboutme:https://davidkingzyb.tech\n"

#手动录像脚本路径
manual_tmpl_path='./douyutv.py'
now_tmpl_path='xxx'
douyutv_plug_path='/Library/Python/2.7/site-packages/streamlink/plugins/douyutv.py'
```

## Usage

### 上线通知 & 录像 & 弹幕抓取

`$ sh run.sh`

### 自动录像

`$ nohup python3 pccold.py &`

### 弹幕抓取

`$ nohup python3 danmu.py >/dev/null 2>&1 &`

### 下载斗鱼视频

编辑下载列表
格式`[文件名](URL路径)`

`$ nohup python3 videodownload.py &`








