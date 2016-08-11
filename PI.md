```

$ sudo mount -t auto -o uid=pi,gid=pi /dev/sda2 /media/usbhdd


# start

$ nohup python pccold.py &
$ exit



# stop

$ ps aux | grep pccold
$ ps aux | grep livestreamer
$ kill -9 PID


```