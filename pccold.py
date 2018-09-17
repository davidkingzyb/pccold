# coding: utf-8
"""
===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2018/1/2 by DKZ https://davidkingzyb.github.io

"""

import json
import time
import subprocess
import threading
import logging
import sys
import os
import signal
import traceback
import re
import requests

import conf
import tools

#log set
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%m/%d %H:%M:%S',
                filename='coldlog.log',
                filemode='w')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)


def saveStream(level,room_obj):
    logging.info('saveStream')
    now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
    room_name=re.sub(r'[\\/:*?"< >()|]','',room_obj['data']['room_name'].replace(' ','_').replace(':','_'))
    file_name=room_name+now_time+'.mp4'
    cmd='streamlink -o "'+conf.download_path+'/'+file_name+'" '+conf.room_url+str(conf.room_num)+' '+level#+' &'
    shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('save start pid='+str(shell.pid))
    logging.info('$ '+cmd)
    sleepkiller=SleepKillerThread(shell)
    returncode_observer=ReturnCodeObserverThread(shell)
    returncode_observer.sleepkiller=sleepkiller


class ReturnCodeObserverThread():
    shell=None
    thread=None
    sleepkiller=None

    def __init__(self,shell):
        self.shell=shell
        self.thread=threading.Thread(target=self.returnCodeObserver)
        self.thread.start()

    def returnCodeObserver(self):
        logging.info('returnCodeObserver')
        returncode=self.shell.wait()
        logging.info('save quit pid='+str(self.shell.pid)+' return code='+str(returncode))
        if returncode!=-9:
            self.sleepkiller.stop()
            time.sleep(30)
            logging.info('start main from return code observer')
            main()

class SleepKillerThread():
    isstoped=False
    shell=None
    thread=None

    def __init__(self,shell):
        self.shell=shell
        self.thread=threading.Thread(target=self.sleepKiller)
        self.thread.start()

    def stop(self):
        self.isstoped=True

    def sleepKiller(self):
        logging.info('sleepKiller')
        time.sleep(conf.how_long)
        if self.isstoped:
            return
        t=threading.Thread(target=main)
        t.start()
        time.sleep(60)
        if self.isstoped:
            return
        try:
            os.killpg(os.getpgid(self.shell.pid),signal.SIGKILL)
            logging.info('save end '+str(self.shell.pid))
        except Exception as e:
            logging.info('*** save end err '+str(self.shell.pid))

def sendEmails(room_obj):
    logging.info('sendEmails')
    try:
        email_obj=tools.initPcColdEmail(room_obj)
        tools.sendEmail(email_obj['subj'],conf.my_email,email_obj['body'],conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception as e:
        logging.warning('*** fail send email')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)

def doBypy():
    logging.info('doBypy')
    date_time=time.strftime('_%Y_%m_%d_%H_%M',time.localtime(time.time()))
    cmd='cd '+conf.download_path+';cp ../coldlog.log coldlog'+date_time+'.log;bypy upload'
    logging.info('$ '+cmd)
    shell=subprocess.Popen(cmd,shell=True)

is_live=False

def main(): 
    try:
        sys.stdout.write('+')
        sys.stdout.flush()
        room_obj=tools.testRoomStatus()
        global is_live
        if room_obj:
            logging.info('live on')
            if not is_live:
                is_live=True
                t=threading.Thread(target=sendEmails,args=(room_obj,))
                t.start()
            saveStream(conf.stream_type,room_obj)
        else:
            if is_live:
                is_live=False
                doBypy()
            sys.stdout.write('-')
            sys.stdout.flush()
            time.sleep(60)
            t=threading.Thread(target=main)
            t.start()
    except Exception as e:
        logging.warning('*** main fail')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)
        time.sleep(60)
        tt=threading.Thread(target=main)
        tt.start()

if __name__ == '__main__':
    logging.info('start pccold')
    main()
