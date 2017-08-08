# coding: utf-8

import subprocess
import smtplib
from email.mime.text import MIMEText
import urllib2
import time
import conf

def sendEmail(subj,to,body,sender,passwd,host,port=25):
    msg=MIMEText(body,'plain','utf-8')
    msg['subject']=subj
    msg['from']=sender
    msg['to']=to

    server=smtplib.SMTP(host,port)
    server.login(sender,passwd)
    server.sendmail(sender,to,msg.as_string())
    server.quit()

def initPcColdEmail(roomobj):
    subj='[pccold]'+roomobj['data']['room_name']+'@'+roomobj['data']['owner_name']
    body='\nroom_name:'+roomobj['data']['room_name']
    body+='\nowner_name:'+roomobj['data']['owner_name']+'#'+roomobj['data']['room_id']
    body+='\nstart_time:'+roomobj['data']['start_time']
    body+='\ncate_name:'+roomobj['data']['cate_name']
    body+='\nlink:http://www.douyutv.com/'+roomobj['data']['room_id']
    #body+=pccoldfooter
    body+=conf.pccold_contact
    return {'body':body,'subj':subj}

def doBypy(download_path):
    date_time=time.strftime('_%Y_%m_%d_%H_%M',time.localtime(time.time()))
    cmd='cd '+download_path+';cp ../coldlog.log coldlog'+date_time+'.log;bypy upload'
    shell=subprocess.Popen(cmd,shell=True)

def spider(url,cookie='',ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'):
    req=urllib2.Request(url)
    req.add_header('Cookie',cookie)
    req.add_header('User-Agent',ua)
    resp=urllib2.urlopen(req)
    html=resp.read()
    return html

def read(file):
    with open(file,'r') as f:
        return f.read()

def write(file,str):
    with open(file,'w') as f:
        f.write(str)