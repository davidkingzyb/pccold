# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import time
import requests
import json

import conf

requests.adapters.DEFAULT_RETRIES = 3

def testRoomStatus():
    s=requests.session()
    s.keep_alive=False
    room_obj=s.get(conf.room_api+str(conf.room_num)).json()
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