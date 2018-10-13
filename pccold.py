# coding: utf-8
"""
===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2018/10/5 by DKZ https://davidkingzyb.tech

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

from tools import sendEmails,doBypy,saveStream,testRoomStatus,pidpool,ReturnCodeObserverThread,SleepKillerThread

is_live=False

def main(): 
    try:
        room_obj=testRoomStatus()
        global is_live
        if room_obj.get('room_status')=="1":
            logging.info('live on')
            if not is_live:
                is_live=True
                t=threading.Thread(target=sendEmails,args=(room_obj,))
                t.start()
            now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
            room_name=room_obj.get('room_name','default').replace(' ','_').replace(':','_')
            saveStream(conf.stream_type,room_name+now_time+'.mp4')
        elif room_obj.get('room_status')=="2":
            if is_live:
                is_live=False
                if conf.is_bypy:
                    doBypy()
            time.sleep(90)  
            tt=threading.Thread(target=main)
            tt.start()
        else:
            time.sleep(90)
            tt=threading.Thread(target=main)
            tt.start()
    except Exception as e:
        logging.warning('*** main fail')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)
        pp=pidpool.copy()
        for k,v in pp.items():
            try:
                os.killpg(os.getpgid(int(k)),signal.SIGKILL)
                logging.info('main kill '+k)
            except Exception as e:
                logging.info('*** main kill err '+k)
        time.sleep(60)
        ttt=threading.Thread(target=main)
        ttt.start()

ReturnCodeObserverThread.main=main
SleepKillerThread.main=main

if __name__ == '__main__':
    logging.info('start pccold')
    main()
