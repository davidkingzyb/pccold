import websocket
import socket
import time
from websocket import create_connection,WebSocket
import pystt
import threading
from .config import conf
from .tail_call import tail_call_optimized
from .tools import sendEmail

luckystar=0
keybody=''

def chatMsgFillter(txt,uname,uid):
    global keybody
    keywordlist=conf.keyword.split(',')
    for w in keywordlist:
        if w in txt:
            keybody+=uid+' @ '+uname+' : '+txt+'\n'
    if uname==conf.keyuser or uid==conf.keyuid:
        keybody+=uid+' @ '+uname+' : '+txt+'\n'
    # ⭐ 🌟
    global luckystar
    if '⭐' in txt or '🌟' in txt:
        if luckystar<5 and luckystar>=0:
            luckystar+=1
        elif luckystar>=5: 
            luckystar=-1
            print('### luckystar ###')
            t=threading.Thread(target=sendEmail,args=('[pccold]Lucky Star',conf.my_email,conf.env+'\n'+conf.pccold_contact,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port,))
            t.start()



class DouyuMsg(object):

    def __init__(self,obj=None,content=None,message=None):
        if obj:
            self.obj=obj
            self.content=pystt.dumps(obj)
            self.contentToMessage()  
        if content:
            self.content=content
            self.contentToMessage()  
        if message:
            self.message=message
            self.messageToContent()
            self.contentToObj()

    def contentToMessage(self):
        self.length = bytearray([len(self.content) + 9, 0x00, 0x00, 0x00])
        self.code = self.length
        self.magic = bytearray([0xb1, 0x02, 0x00, 0x00])
        self.contentb = bytes(self.content.encode("utf-8"))
        self.end = bytearray([0x00])
        self.message=bytes(self.length + self.code + self.magic + self.contentb + self.end)
        return self.message 

    def getMessage(self):
        return self.message 

    def messageToContent(self):
        self.content=self.message[12:-1].decode(encoding='utf-8',errors='ignore')
        return self.content

    def contentToObj(self):
        self.obj=pystt.loads(self.content)
        return self.obj

    def getObj(self):
        return self.obj

    def getInfo(self):
        if self.obj.get('type')=='chatmsg':
            chatMsgFillter(self.obj.get('txt',''),self.obj.get('nn',''),self.obj.get('uid',''))
            return self.obj.get('uid','')+' @ '+self.obj.get('nn','')+' : '+self.obj.get('txt','')
        elif self.obj.get('type')=='uenter':
            if self.obj.get('uid','')==conf.keyuid or self.obj.get('nn','')==conf.keyuser:
                print('### PcCold Enter ###')
                t=threading.Thread(target=sendEmail,args=('[pccold]'+conf.keyuser+' Enter',conf.my_email,conf.env+'\n'+conf.pccold_contact,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port,))
                t.start()
            return self.obj.get('uid','')+' @ '+self.obj.get('nn','')+' @ uenter'
        elif self.obj.get('type')=='rss':
            global keybody
            t=threading.Thread(target=sendEmail,args=('[pccold]Live',conf.my_email,conf.env+'\n\n\n'+keybody+'\n\n\n'+conf.pccold_contact,conf.mail_sender,conf.mail_passwd,conf.mail_host,conf.mail_port,))
            t.start()
            keybody=''
            return '### Live ###'
        elif self.obj.get('type') in 'dgb,wiru,rankup,actfsts1od_r,frank,rri,svsnres,newblackres,fire_user,fire_start,tsboxb,ghz2019arkcalc,ghz2019s1info,ghz2019s2info,fire_real_user,gbroadcast,srres,spbc,ghz2019s2calc,upgrade,rquizisn,anbc,wirt,ghz2019s1disp,blab,cthn,rnewbc,noble_num_info,rank_change,mrkl,synexp,fswrank,ranklist,qausrespond':
            return None
        else:
            print('*** '+self.obj.get('type')+' ***')
            return None


def login(ws,room_id,username,uid):
    req={
        'type':'loginreq',
        'room_id':room_id,
        'dfl':'sn@A=105@Sss@A=1',
        'username':username,
        'uid':uid,
        'ver':'20190610',
        'aver':'218101901',
        'ct':'0'
    }
    print('### login ###',req)
    binary=DouyuMsg(req).getMessage()
    ws.send(binary)

def join(ws,room_id):
    req={
        'type':'joingroup',
        'rid':room_id,
        'gid':'1'
    }
    print('### join ###',req)
    binary=DouyuMsg(req).getMessage()
    ws.send(binary)

@tail_call_optimized
def mrkl(ws):
    global luckystar
    luckystar=0
    req={
        'type':'mrkl'
    }
    binary=DouyuMsg(req).getMessage()
    now_time=time.strftime('## %m_%d_%H_%M ##',time.localtime(time.time()))
    print(now_time)
    try:
        ws.send(binary)
        time.sleep(40)
        return mrkl(ws)
    except Exception as err:
        print('** mrkl error **')


def keepalive(ws):
    t=threading.Thread(target=mrkl,args=(ws,))
    t.start()

def on_message(ws, message):
    try:
        info=DouyuMsg(message=message).getInfo()
        if info:
            print(info)
    except Exception as err:
        print('** message parse err **')
        print(message,err)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    return wsdanmumain()

def on_open(ws):
    print('### open ###')
    login(ws,str(conf.room_num),conf.username,conf.uid)
    join(ws,str(conf.room_num))
    keepalive(ws)

@tail_call_optimized
def wsdanmumain():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://danmuproxy.douyu.com:8503/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    wsdanmumain()
