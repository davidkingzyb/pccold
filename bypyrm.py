# 2018/12/31 by DKZ

from tools import sendEmail
import conf
import psutil
import subprocess
import logging

def doBypy():
    logging.info('doBypy')
    cmd='cd '+conf.download_path+';bypy upload'
    logging.info('$ '+cmd)
    shell=subprocess.Popen(cmd,shell=True)
    return shell

def psCheck(name):
    result=[p.info for p in psutil.process_iter(attrs=['pid', 'name']) if name in p.info['name']]
    return result

def initBypyRmEmail(body):
    subj='[pccold] bypyrm'
    logging.info('[bypyrm] '+body)
    try:
        sendEmail(subj,conf.my_email,body,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception as e:
        logging.info('*** email fail',e)

def bypyrm():
    logging.info('start bypyrm')
    if not psCheck('bypy') and not psCheck('streamlink'):
        shell=doBypy()
        returncode=shell.wait()
        if returncode==0:
            cmd='cd '+conf.download_path+';rm *.mp4'
            p=subprocess.Popen(cmd,shell=True)
            initBypyRmEmail('ok')
        else:
            initBypyRmEmail('fail '+str(returncode))
    else:
        initBypyRmEmail('psCheck process is runing')


if __name__ == '__main__':
    bypyrm()     