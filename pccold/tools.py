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
import traceback
from .config import conf

pidpool={}

def sendEmails(room_obj):
    global conf
    logging.info('sendEmails')
    try:
        email_obj=initPcColdEmail(room_obj)
        sendEmail(email_obj['subj'],conf.my_email,email_obj['body'],conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception as e:
        logging.warning('*** fail send email')
        logging.warning(e)
        tb=traceback.format_exc()
        logging.warning(tb)

def saveStream(level,file_name,url):
    global conf
    url=url or "https://www.douyu.com/"+str(conf.room_id)
    logging.info('saveStream')
    cmd='pccoldcli '+conf.download_path+'/'+file_name
    shell=subprocess.Popen(cmd,shell=True,preexec_fn=os.setsid)
    logging.info('save start pid='+str(shell.pid))
    logging.info('$ '+cmd)
    sleepkiller=SleepKillerThread(shell)
    returncode_observer=ReturnCodeObserverThread(shell)
    returncode_observer.sleepkiller=sleepkiller
    sleepkiller.return_code_observer=returncode_observer
    global pidpool
    pidpool[str(shell.pid)]=True


class ReturnCodeObserverThread():
    isstoped=False
    shell=None
    thread=None
    sleepkiller=None

    def __init__(self,shell):
        self.shell=shell
        self.thread=threading.Thread(target=self.returnCodeObserver)
        self.thread.start()

    def stop(self):
        self.isstoped=True

    def returnCodeObserver(self):
        logging.info('returnCodeObserver')
        returncode=self.shell.wait()
        global pidpool
        del pidpool[str(self.shell.pid)]
        self.sleepkiller.stop()
        logging.info('save quit pid='+str(self.shell.pid)+' return code='+str(returncode))
        if returncode!=-9 and not self.isstoped:
            time.sleep(60)
            logging.info('start main from return code observer')
            ReturnCodeObserverThread.main()

class SleepKillerThread():
    isstoped=False
    shell=None
    thread=None
    return_code_observer=None

    def __init__(self,shell):
        self.shell=shell
        self.thread=threading.Thread(target=self.sleepKiller)
        self.thread.start()

    def stop(self):
        self.isstoped=True

    def sleepKiller(self):
        global conf
        if not conf.is_cut:
            return
        logging.info('sleepKiller')
        time.sleep(conf.how_long)
        if self.isstoped:
            return
        t=threading.Thread(target=SleepKillerThread.main)
        t.start()
        self.return_code_observer.stop()
        time.sleep(60)
        try:
            os.killpg(os.getpgid(self.shell.pid),signal.SIGKILL)
            logging.info('save end '+str(self.shell.pid))
        except Exception as e:
            logging.info('*** save end err '+str(self.shell.pid))


def testRoomStatus():
    global conf
    try:
        room_obj=requests.get("https://www.douyu.com/betard/"+str(conf.room_id),timeout=10).json()
        result=room_obj.get('room',{'show_status':0})
        return result
    except Exception as e:
        logging.info('*** test room status err')
        return {'show_status':0}

def initPcColdEmail(roomobj):
    global conf
    subj='[pccold]'+roomobj.get('room_name')+'@'+roomobj.get('nickname')
    body='\nenv:'+conf.env
    body+='\nroom_name:'+roomobj.get('room_name')
    body+='\nowner_name:'+roomobj.get('owner_name')+'#'+str(roomobj.get('room_id'))
    t=time.localtime(roomobj.get('show_time'))
    start_time=time.strftime("%Y-%m-%d %H:%M:%S", t)
    body+='\nstart_time:'+start_time
    body+='\nsecond_lvl_name:'+roomobj.get("second_lvl_name")
    body+='\nlink:http://www.douyutv.com/'+str(roomobj.get('room_id'))
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