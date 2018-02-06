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
import streamlink

#log set
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%m/%d %H:%M:%S',
                filename='coldlog.log',
                filemode='w')
#console = logging.StreamHandler()
#console.setLevel(logging.INFO)
#formatter = logging.Formatter('%(name)-12s: %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)

def doStream(room_obj):
    logging.info('doStream')
    streams = streamlink.streams(conf.room_url+str(conf.room_id))
    if conf.stream_type in streams.keys():
        saveStream(conf.stream_type,room_obj)
    else:
        if len(streams.keys())>0:
            saveStream(streams.keys()[0],room_obj)
        else:
            saveStream('source',room_obj)


def saveStream(level,room_obj):
    logging.info('saveStream')
    now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
    room_name=re.sub(r'[\\/:*?"< >()|]','',room_obj['data']['room_name'].replace(' ','_').replace(':','_'))
    file_name=room_name+now_time+'.mp4'
    cmd='streamlink -o "'+conf.download_path+'/'+file_name+'" '+conf.room_url+conf.room_id+' '+level#+' &'
    shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('$ '+cmd)
    sleepKiller(shell)

def sleepKiller(shell):
    time.sleep(conf.how_long)
    t=threading.Thread(target=main)
    t.start()
    time.sleep(60)
    os.killpg(os.getpgid(shell.pid),signal.SIGINT)
    logging.info('save end '+str(shell.pid))

def sendEmails(room_obj):
    logging.info('sendEmails')
    try:
        email_obj=tools.initPcColdEmail(room_obj)
        tools.sendEmail(email_obj['subj'],conf.my_email,email_obj['body'],conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception,e:
        logging.warning('*** fail send email')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)

def doBypy():
    logging.info('doBypy')
    date_time=time.strftime('_%Y_%m_%d_%H_%M',time.localtime(time.time()))
    cmd='cd '+conf.download_path+';mv ../coldlog.log coldlog'+date_time+'.log;bypy upload'
    logging.info('$ '+cmd)
    shell=subprocess.Popen(cmd,shell=True)

is_live=False

def main(): 
    try:
        room_obj=tools.testRoomStatus()
        global is_live
        if room_obj:
            logging.info('live on')
            if not is_live:
                is_live=True
                t=threading.Thread(target=sendEmails,args=(room_obj,))
                t.start()
            doStream(room_obj)
        else:
            if is_live:
                is_live=False
                doBypy()
            sys.stdout.write('-')
            sys.stdout.flush()
            time.sleep(60)
            t=threading.Thread(target=main)
            t.start()
    except Exception,e:
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
