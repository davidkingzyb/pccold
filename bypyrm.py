# 2018/12/31 by DKZ

from tools import sendEmail,doBypy
import conf
import psutil
import subprocess


def psCheck(name):
    result=[p.info for p in psutil.process_iter(attrs=['pid', 'name']) if name in p.info['name']]
    return result

def initBypyRmEmail(body):
    subj='[pccold] bypyrm'
    print('[bypyrm] '+body)
    try:
        sendEmail(subj,conf.my_email,body,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port)
    except Exception as e:
        print('*** email fail',e)

def main():
    print('start bypyrm')
    if not psCheck('bypy') and not psCheck('streamlink'):
        shell=doBypy()
        returncode=shell.wait()
        if returncode==0:
            cmd='cd '+conf.download_path+';rm *.mp4'
            p=subprocess.Popen(cmd,shell=True)
            initBypyRmEmail('ok')
        else:
            initBypyRmEmail('fail '+returncode)
    else:
        initBypyRmEmail('psCheck process is runing')


if __name__ == '__main__':
    main()
