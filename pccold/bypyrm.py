# 2018/12/31 by DKZ

from .tools import sendEmail
import psutil
import subprocess
import logging
from .config import conf


def doBypy():
    global conf
    logging.info('doBypy')
    cmd='cd '+conf.download_path+';bypy upload'
    logging.info('$ '+cmd)
    shell=subprocess.Popen(cmd,shell=True)
    return shell

def psCheck(name):
    result=[p.info for p in psutil.process_iter(attrs=['pid', 'name']) if name in p.info['name']]
    return result

def initBypyRmEmail(body):
    global conf
    subj='[pccold] bypyrm '+body
    logging.info('[bypyrm] '+body)
    try:
        sendEmail(subj,conf.my_email,body+'\n'+conf.env+'\n'+conf.pccold_contact,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception as e:
        logging.info('*** email fail',e)

def bypyrm():
    global conf
    logging.info('start bypyrm')
    if not psCheck('bypy') and not psCheck('streamlink'):
        shell=doBypy()
        returncode=shell.wait()
        if returncode==0:
            cmd='cd '+conf.download_path+';rm *.mp4'
            p=subprocess.Popen(cmd,shell=True)
            if conf.bypy_mail:
                initBypyRmEmail('ok')
        else:
            initBypyRmEmail('fail '+str(returncode))
    else:
        initBypyRmEmail('psCheck process is runing')


if __name__ == '__main__':
    bypyrm()     