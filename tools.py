# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import time
import requests
import json
import subprocess
import threading
import os
import signal
import logging

import conf

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

pidpool={}

def sendEmails(room_obj):
    logging.info('sendEmails')
    try:
        email_obj=initPcColdEmail(room_obj)
        sendEmail(email_obj['subj'],conf.my_email,email_obj['body'],conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
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

def saveStream(level,file_name,url=conf.room_url+str(conf.room_num)):
    logging.info('saveStream')
    cmd='streamlink -o "'+conf.download_path+'/'+file_name+'" '+url+' '+level#+' &'
    shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('save start pid='+str(shell.pid))
    logging.info('$ '+cmd)
    sleepkiller=SleepKillerThread(shell)
    returncode_observer=ReturnCodeObserverThread(shell)
    returncode_observer.sleepkiller=sleepkiller
    global pidpool
    pidpool[str(shell.pid)]=True


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
        global pidpool
        del pidpool[str(self.shell.pid)]
        self.sleepkiller.stop()
        logging.info('save quit pid='+str(self.shell.pid)+' return code='+str(returncode))
        if returncode!=-9:
            time.sleep(60)
            logging.info('start main from return code observer')
            ReturnCodeObserverThread.main()

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
        if self.isstoped or not conf.is_cut:
            return
        logging.info('sleepKiller')
        time.sleep(conf.how_long)
        t=threading.Thread(target=SleepKillerThread.main)
        t.start()
        time.sleep(60)
        try:
            os.killpg(os.getpgid(self.shell.pid),signal.SIGKILL)
            logging.info('save end '+str(self.shell.pid))
        except Exception as e:
            logging.info('*** save end err '+str(self.shell.pid))


def testRoomStatus():
    room_obj=requests.get(conf.room_api+str(conf.room_num),timeout=10).json()
    if room_obj.get('data',{'room_status':'0'}).get('room_status','0')=="1":
        return room_obj
    else:
        return None

def initPcColdEmail(roomobj):
    subj='[pccold]'+roomobj['data']['room_name']+'@'+roomobj['data']['owner_name']
    body='\nroom_name:'+roomobj['data']['room_name']
    body+='\nowner_name:'+roomobj['data']['owner_name']+'#'+roomobj['data']['room_id']
    body+='\nstart_time:'+roomobj['data']['start_time']
    body+='\ncate_name:'+roomobj['data']['cate_name']
    body+='\nlink:http://www.douyutv.com/'+roomobj['data']['room_id']
    body+=conf.pccold_contact
    return {'body':body,'subj':subj}

def sendEmail(subj,to,body,sender,passwd,host,port=25):
    msg=MIMEText(body,'plain','utf-8')
    msg['subject']=subj
    msg['from']=sender
    msg['to']=to

    server=smtplib.SMTP(host,port)
    server.login(sender,passwd)
    server.sendmail(sender,to,msg.as_string())
    server.quit()

def read(file):
    with open(file,'r') as f:
        return f.read()

def write(file,str):
    with open(file,'w') as f:
        f.write(str)

if __name__ == '__main__':
    testRoomStatus()