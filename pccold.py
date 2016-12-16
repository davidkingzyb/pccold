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
power="livestreamer"
# power="you-get"

#path="/media/usbhdd/colddownload"
path="./download"
roomid="cold"
streamtype='middle'

setHowLong=True
pikll=True
howlong=60*30 #30min

isSendMail=True
isBypy=True

roomapi='http://open.douyucdn.cn/api/RoomApi/room/'
roomurl="http://www.douyutv.com/"
myemail="zaowuworld@163.com"


# roomid="kpc"  #test




import livestreamer
import sendEmail
import spiderman
import json
import time
import subprocess
import threading
import sys
import logging
import os
import signal
import traceback


#log set
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                filename='coldlog.log',
                filemode='w')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

date=time.strftime('%Y_%m_%d_%H_%M',time.localtime(time.time()))
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
        global date
        logging.info(str(date)+'test room status on(1) roomid='+roomid)
        return obj
    else:
        sys.stdout.write('-')
        sys.stdout.flush()
        global isSendMail
        global isBypy
        if isSendMail==False:
            isSendMail=True
            if isBypy:
                try:
                    dates=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
                    logging.info('============$ bypy upload===========')
                    bypycmd='cd ~/workspace/pccold/download;cp ../coldlog.log cold'+dates+'.log;bypy upload'
                    logging.info(bypycmd)
                    shell=subprocess.Popen(bypycmd,shell=True)
                    logging.info('---------------bypy uploading-----------------')
                except Exception,e:
                    logging.warning('========bypy upload fail=======')
                    logging.warning(e)
                    tb=traceback.format_exc()
                    logging.warning(tb)
                    logging.warning('---------------------------------------')
        time.sleep(60)
        t=threading.Thread(target=main)
        t.start()
        return

def savelivestreamer(roomid,streams,objstr):
    if streamtype in streams.keys():
        p=streamtype
    elif 'source' in streams.keys():
        p='source'
    else:
        p=streams.keys()[0]
    logging.info('save '+p+'#'+objstr)
    now=time.strftime('%Y_%m_%d_%H_%M',time.localtime(time.time()))
    filename=objstr+now+'.mp4'
    cmd='livestreamer -o "'+path+'/'+filename+'" '+roomurl+roomid+' '+p#+' &'
    shell=subprocess.Popen(cmd,shell=True)
    logging.info('do:'+cmd+' pid:'+str(shell.pid))

    if setHowLong:
        # time limit
        time.sleep(howlong)
        t=threading.Thread(target=main)
        t.start()
        time.sleep(60)
        shell.kill()
        logging.info('save end '+str(shell.pid)+' '+filename)
        if pikll:
            # pi
            kll=subprocess.Popen('kill -9 '+str(shell.pid+1),shell=True)


def saveyouget(roomid):
    cmd='you-get -o '+path+' '+roomurl+roomid
    shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('do:'+cmd+' pid:'+str(shell.pid))
    if setHowLong:
        time.sleep(howlong)
        t=threading.Thread(target=main)
        t.start()
        time.sleep(15)
        # shell.kill()
        os.killpg(os.getpgid(shell.pid),signal.SIGTERM)
        logging.info('save end '+str(shell.pid))



def main():
    global isSendMail
    try:
        obj=testroomstatus(roomid)

        if obj:   
            #sendEmail
            objstr=obj['data']['room_name']  #+'_'+obj['data']['start_time']+'_'+obj['data']['owner_name']
            logging.info('====================== info ==========================')
            logging.info('[pccold]'+obj['data']['room_name']+'    @ '+obj['data']['owner_name']+' # '+obj['data']['start_time']);
            logging.info('======================================================')
            try:
                if isSendMail:
                    sendEmail.pccold(obj,myemail)
                    isSendMail=False
                    logging.info('send email to '+myemail)
            except Exception,e:
                logging.warning('=========fail send email===============')
                logging.warning(e)
                # traceback.print_exc()
                tb=traceback.format_exc()
                logging.warning(tb)
                logging.warning('---------------------------------------')
            
            if power=='livestreamer':
                #get steams
                streams=getStream(roomid)
                if streams:
                    savelivestreamer(roomid,streams,objstr.replace(' ','_').replace(':','_'))
            elif power=='you-get':
                #you-get
                saveyouget(roomid)


    except Exception,e:
        logging.warning('===========restart=========')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)
        logging.warning('---------------------------')
        time.sleep(60)
        main()
    


    


if __name__ == '__main__':
    logging.info('====start pccold '+date+'====')
    main()


