# pccold

**douyu 主播上线通知 & 视频自动录制**

2016/8/10 by DKZ



主播上线邮件通知，并且自动录制视频。

## Install

- python2.7
- [livestreamer](https://github.com/chrippa/livestreamer)
- [streamlink](https://github.com/streamlink/streamlink)
- [you-get](https://github.com/soimort/you-get)
- [ffmpeg](https://www.ffmpeg.org/)

## Set

```
$ vi conf.py

# conf.py

# power="livestreamer"
# power="you-get"
power="streamlink"

download_path="./download"
stream_type='middle'

is_set_how_long=True
is_plus_kill=True
how_long=60*30 #30min

is_send_mail=True
is_bypy=True

my_email="zaowuworld@163.com"

room_api='http://open.douyucdn.cn/api/RoomApi/room/'
room_url="http://www.douyutv.com/"
room_id="cold"
room_id='kpc'#test

mail_sender='xxx'
mail_passwd='xxx'
mail_host='xxx'
mail_port=25 #exmail.qq 465 or 25

pccold_contact="\npccold by DKZ \n---------------------\ngithub:https://github.com/davidkingzyb/pccold\ncontact:davidkingzyb@163.com  @__DKZ__\naboutme:http://davidkingzyb.github.io\n"

```

## Usage

```
$ python pccold.py

# or
$ nohup python pccold.py &
```

**fix mp4 processbar use [ffmpeg](https://www.ffmpeg.org/)**

```
$ ffmpeg -i input.mp4 -t 00:31:00 output.mp4
```



