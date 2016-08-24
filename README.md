# pccold

**douyu 主播上线通知 & 视频自动录制**

2016/8/10 by DKZ



主播上线邮件通知，并且自动录制视频。

power by [livestreamer](https://github.com/chrippa/livestreamer)

##Install

- python2.7
- [livestreamer](https://github.com/chrippa/livestreamer)

**use develope version [steven7851's plug](https://github.com/steven7851/livestreamer/blob/2ee1b8f72924c4aa40da700529af0bc4386f01c6/src/livestreamer/plugins/douyutv.py)**

##Set

```
$ vi dkzsecret.py

#dkzsecret.py

mailsender='youremail'
mailpwd='yourpassword'
mailhost='stmpserver'

#pccold.py

path="./download/"   #your path
roomid="cold"        #room id
streamtype='middle'  

setHowLong=True
pikll=False          #linux kill livestreamer
howlong=60*30        #30min

isSendMail=True      #send email

```

##Usage

```
$ python pccold.py

# or
$ nohup python pccold.py &
```

**linux use pipccold.py**

```
# for pi

$ sudo mount /dev/sda2 /media/usbhdd

# start

$ nohup python pipccold.py &
$ exit

# stop

$ ps aux | grep pccold
$ ps aux | grep livestreamer
$ kill -9 PID

# tar
$ tar -cv colddownload -f coldtar.tar

$ umount /media/usbhdd
```

**fix mp4 processbar use [ffmpeg](https://www.ffmpeg.org/)**

```
$ ffmpeg -i input.mp4 -t 00:31:00 output.mp4
```



