# coding: utf-8
"""

===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2016/08/08 by DKZ https://davidkingzyb.github.io

"""

path="/media/usbhdd/colddownload/"
roomid="cold"
howlong=60*30 #30min

roomapi='http://open.douyucdn.cn/api/RoomApi/room/'
roomurl="http://www.douyutv.com/"
myemail="zaowuworld@163.com"

# test
# roomid="kpc"
path="./download/"



import livestreamer
import sendEmail
import spiderman
import json
import datetime
import time
import subprocess
import threading
import sys
import logging


#log set
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                filename='coldlog.log',
                filemode='w')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

date=datetime.datetime.now().strftime('%Y_%m_%d')

def getStream(roomid):
    streams = livestreamer.streams(roomurl+str(roomid))
    if len(streams)>0:
        return streams
    else:
        logging.info('no streams')
        time.sleep(10)
        main()
        return
        

def testroomstatus(roomid):
    resp=spiderman.spider(roomapi+str(roomid))
    obj=json.loads(resp)
    if obj['data']['room_status']=='1':
        logging.info(str(date)+'test room status on(1) roomid='+roomid)
        return obj
    else:
        sys.stdout.write('-')
        sys.stdout.flush()
        time.sleep(60)
        t=threading.Thread(target=main)
        t.start()
        return

def savestream(roomid,streams,objstr):
    if 'source' in streams.keys():
        p='source'
    elif 'best' in streams.keys():
        p='best'
    elif 'middle' in streams.keys():
        p='middle'
    else:
        p=streams.keys()[0]
    logging.info('save '+p+'#'+objstr)
    now=datetime.datetime.now().strftime('_%I_%M')
    filename=objstr+now+'.mp4'
    cmd='livestreamer -o "'+path+filename+'" '+roomurl+roomid+' '+p#+' &'
    logging.info('do '+cmd)
    shell=subprocess.Popen(cmd,shell=True)
    time.sleep(howlong)
    t=threading.Thread(target=main)
    t.start()
    time.sleep(10)
    shell.kill()
    logging.info('save end'+filename)


def main():
    try:
        obj=testroomstatus(roomid)

        if obj:   
            #sendEmail
            try:
                objstr=obj['data']['owner_name']+'_'+obj['data']['start_time']+'_'+obj['data']['room_id']
                body='from pccold project by DKZ\n\n'+objstr
                sendEmail.sendEmail(objstr,myemail,body)
                logging.info('send email to '+myemail)
            except Exception,e:
                logging.warning('*fail send email*')
                logging.warning(e)
            
            #get steams
            streams=getStream(roomid)
            if streams:
                savestream(roomid,streams,objstr.replace(' ','_'))

    except Exception,e:
        logging.warning('*restart*')
        logging.warning(e)
        time.sleep(60)
        main()
    


    


if __name__ == '__main__':
    logging.info('====start pccold '+date+'====')
    main()


