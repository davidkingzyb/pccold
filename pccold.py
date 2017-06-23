# coding: utf-8
"""
===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2017/06/23 by DKZ https://davidkingzyb.github.io

"""

import json
import time
import subprocess
import threading
import sys
import logging
import os
import signal
import traceback
import re

import conf
import tools

#log set
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                filename='coldlog.log',
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

date_time=time.strftime('%Y_%m_%d_%H_%M',time.localtime(time.time()))

is_send_mail=conf.is_send_mail
is_bypy=conf.is_bypy

def saveYouGet(room_obj):
    cmd='you-get -o '+conf.download_path+' '+conf.room_url+conf.room_id
    # shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('==== save you-get ====')
    logging.info('$ '+cmd+' @ pid:'+str(shell.pid))
    # if conf.is_set_how_long:
        # sleepKiller(shell)

def saveLiveStreamer(room_obj):
    import livestreamer
    streams = livestreamer.streams(conf.room_url+str(conf.room_id))
    if conf.stream_type in streams.keys():
        level=conf.stream_type
    else:
        level=streams.keys()[0]
    now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
    room_name=re.sub(r'[\\/:*?"< >()|]','',room_obj['data']['room_name'])
    file_name=room_name+now_time+'.mp4'
    cmd='livestreamer -o "'+conf.download_path+'/'+file_name+'" '+conf.room_url+conf.room_id+' '+level#+' &'
    # shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('==== save livestreamer ====')
    logging.info('$ '+cmd+' @ pid:'+str(shell.pid))
    # if conf.is_set_how_long:
        # sleepKiller(shell)

def saveStreamLink(room_obj):
    # import streamlink
    # streams = streamlink.streams(conf.room_url+str(conf.room_id))
    # if conf.stream_type in streams.keys():
    #     level=conf.stream_type
    # else:
    #     level=streams.keys()[0]
    level='middle'#test
    now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
    room_name=re.sub(r'[\\/:*?"< >()|]','',room_obj['data']['room_name'].replace(' ','_').replace(':','_'))
    file_name=room_name+now_time+'.mp4'
    cmd='streamlink -o "'+conf.download_path+'/'+file_name+'" '+conf.room_url+conf.room_id+' '+level#+' &'
    # shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('==== save streamlink ====')
    logging.info('$ '+cmd)
    # if conf.is_set_how_long:
        # sleepKiller(shell)
        

def sleepKiller(shell):
    time.sleep(conf.how_long)
    t=threading.Thread(target=main)
    t.start()
    time.sleep(60)
    os.killpg(os.getpgid(shell.pid),signal.SIGINT)
    logging.info('save end '+str(shell.pid))
    if conf.is_plus_kill:
        kill=subprocess.Popen('kill -9 '+str(shell.pid+1),shell=True)


def testRoomStatus():
    resp=tools.spider(conf.room_api+str(conf.room_id))
    room_obj=json.loads(resp)
    if room_obj['data']['room_status']=='1':
        global date_time
        logging.info(str(date_time)+'test room status on(1) roomid='+conf.room_id)
        return room_obj
    else:
        sys.stdout.write('-')
        sys.stdout.flush()
        global is_send_mail
        global is_bypy
        if is_send_mail==False:
            is_send_mail=True if conf.is_send_mail else False
            if is_bypy:
                try:
                    logging.info('==== bypy upload ====')
                    tools.doBypy(conf.download_path)
                except Exception,e:
                    logging.warning('*** bypy upload fail ***')
                    logging.warning(e)
                    tb=traceback.format_exc()
                    logging.warning(tb)
        time.sleep(60)
        t=threading.Thread(target=main)
        t.start()
        return

def main(): 
    try:
        room_obj=testRoomStatus()
        if room_obj:
            logging.info('[pccold]'+room_obj['data']['room_name']+' @ '+room_obj['data']['owner_name']+' # '+room_obj['data']['start_time']);
            #send email
            try:
                global is_send_mail
                if is_send_mail:
                    email_obj=tools.initPcColdEmail(room_obj)
                    tools.sendEmail(email_obj['subj'],conf.my_email,email_obj['body'],conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
                    is_send_mail=False
                    logging.info('send email to '+conf.my_email)
            except Exception,e:
                logging.warning('*** fail send email ***')
                logging.warning(e)
                tb=traceback.format_exc()
                logging.warning(tb)
            #save stream
            if conf.power=='livestreamer':
                saveLiveStreamer(room_obj)
            elif conf.power=='you-get':
                saveYouGet(room_obj)
            elif conf.power=='streamlink':
                saveStreamLink(room_obj)
    except Exception,e:
        logging.warning('*** main fail ***')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)
        time.sleep(60)
        main()

if __name__ == '__main__':
    logging.info('==== start pccold '+date_time+' ====')
    main()