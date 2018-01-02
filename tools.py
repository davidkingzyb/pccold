# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import time
import requests
import json

import conf

def testRoomStatus():
    resp=requests.get(conf.room_api+str(conf.room_id)).text
    room_obj=json.loads(resp)
    if room_obj['data']['room_status']=='1':
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