# coding: utf-8
"""

===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2016/08/08 by DKZ https://davidkingzyb.github.io

"""

roomapi='http://open.douyucdn.cn/api/RoomApi/room/'
roomurl="http://www.douyutv.com/"
myemail="davidkingzyb@163.com"
path="./download/"


import livestreamer
import sendEmail
import spiderman
import json
import datetime
import time
import subprocess

date=datetime.datetime.now().strftime('%Y_%m_%d')

def getStream(roomid):
    streams = livestreamer.streams(roomurl+str(roomid))
    if len(streams)>0:
        return streams
    else:
        print('no streams')
        time.sleep(10)
        main()
        

def testroomstatus(roomid):
    resp=spiderman.spider(roomapi+str(roomid))
    obj=json.loads(resp)
    if obj['data']['room_status']=='1':
        print(str(date)+'test room status on(1) roomid='+roomid)
        return obj
    else:
        time.sleep(60)
        testroomstatus(roomid)

def savestream(roomid,streams,objstr):
    if 'source' in streams.keys():
        p='source'
    elif 'best' in streams.keys():
        p='best'
    elif 'middle' in streams.keys():
        p='middle'
    else:
        p=streams.keys()[0]
    print('save '+p+'#'+objstr)
    now=datetime.datetime.now().strftime('_%I_%M')
    filename=objstr+now+'.mp4'
    cmd='livestreamer -o "'+path+filename+'" '+roomurl+roomid+' '+p
    print('do '+cmd)
    shell=subprocess.Popen(cmd,shell=True)
    time.sleep(60)
    shell.kill()
    savestream(roomid,streams,objstr)


def main():
    try:
        obj=testroomstatus('71415')
        
        #sendEmail
        try:
            objstr=obj['data']['owner_name']+'_'+obj['data']['start_time']+'_'+obj['data']['room_id']
            body='from pccold project by DKZ\n\n'+objstr
            sendEmail.sendEmail(objstr,myemail,body)
            print('send email to '+myemail)
        except Exception,e:
            print('*fail send email*')
            print(e)
        
        #get steams
        streams=getStream('71415')
        savestream('71415',streams,objstr.replace(' ','_'))

    except Exception,e:
        print('*restart*')
        print(e)
        time.sleep(60)
        main()
    


    


if __name__ == '__main__':
    main()


