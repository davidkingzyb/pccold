# pccold

**douyu 主播上线通知 & 视频自动录制**

2018/1/4 by DKZ



主播上线邮件通知，并且自动录制视频，上传百度云。

## Dependence

- python
- streamlink
- bypy

## Config

conf.py

```
room_id="cold"
stream_type='medium'
how_long=60*30 #30min

room_api='http://open.douyucdn.cn/api/RoomApi/room/'
room_url="http://www.douyutv.com/"

my_email="xxx@xx.com"
mail_sender='xxx@xxx'
mail_passwd='xx'
mail_host='xx'
mail_port=25 #exmail.qq 465 or 25
pccold_contact="\n\npccold by DKZ \n---------------------\ngithub:https://github.com/davidkingzyb/pccold\ncontact:davidkingzyb@qq.com  @__DKZ__\naboutme:http://davidkingzyb.github.io\n"

download_path="./download"

manual_tmpl_path='./douyutv.py'
now_tmpl_path='./plugs/douyutv.py'
douyutv_plug_path='/Library/Python/2.7/site-packages/streamlink/plugins/douyutv.py'
```

## Usage

```
$ nohup python pccold.py &
```





