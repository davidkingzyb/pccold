import websocket
import socket
import time
from websocket import create_connection,WebSocket
import pystt
import threading
from .config import conf
from .tail_call import tail_call_optimized

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
            return self.obj.get('uid','')+' @ '+self.obj.get('nn','')+' : '+self.obj.get('txt','')
        elif self.obj.get('type')=='uenter':
            return self.obj.get('uid','')+' @ '+self.obj.get('nn','')+' @ uenter'
        elif self.obj.get('type')=='dgb':
            return self.obj.get('uid','')+' @ '+self.obj.get('nn','')+' @ dgb'+' @ '+self.obj.get('gfid')+' @ '+self.obj.get('gs')+' @ '+self.obj.get('gfcnt')
        elif self.obj.get('type') in 'gbroadcast,srres,spbc,ghz2019s2calc,upgrade,rquizisn,anbc,wirt,ghz2019s1disp,blab,cthn,rnewbc,noble_num_info,rank_change,mrkl,synexp,fswrank,ranklist,qausrespond':
            return None
        else:
            print('*** '+self.obj.get('type')+' ***')
            return self.obj


def login(ws,room_id,username,uid):
    # content='type@=loginreq/room_id@='+room_id+'/dfl@=sn@AA=105@ASss@AA=1/username@='+username+'/uid@='+uid+'/ver@=20190610/aver@=218101901/ct@=0/'
    """
00000000: 8b00 0000 8b00 0000 b102 0000 7479 7065  ............type
00000001: 403d 6c6f 6769 6e72 6571 2f72 6f6f 6d69  @=loginreq/roomi
00000002: 6440 3d39 3939 392f 6466 6c40 3d73 6e40  d@=9999/dfl@=sn@
00000003: 4141 3d31 3035 4041 5373 7340 4141 3d31  AA=105@ASss@AA=1
00000004: 2f75 7365 726e 616d 6540 3d76 6973 6974  /username@=visit
00000005: 6f72 3939 3836 3938 372f 7569 6440 3d31  or9986987/uid@=1
00000006: 3136 3736 3134 3839 312f 7665 7240 3d32  167614891/ver@=2
00000007: 3031 3930 3631 302f 6176 6572 403d 3231  0190610/aver@=21
00000008: 3831 3031 3930 312f 6374 403d 302f 00    8101901/ct@=0/.
    """
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
    # req='type@=joingroup/rid@='+room_id+'/gid@=1/'
    """
00000000: 2a00 0000 2a00 0000 b102 0000 7479 7065  *...*.......type
00000001: 403d 6a6f 696e 6772 6f75 702f 7269 6440  @=joingroup/rid@
00000002: 3d39 3939 392f 6769 6440 3d31 2f00       =9999/gid@=1/.    
    """
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
    """
00000000: 1400 0000 1400 0000 b102 0000 7479 7065  ............type
00000001: 403d 6d72 6b6c 2f00                      @=mrkl/.
    """
    # print('### mrkl ###')
    req={
        'type':'mrkl'
    }
    binary=DouyuMsg(req).getMessage()
    ws.send(binary)
    time.sleep(40)
    return mrkl(ws)


def keepalive(ws):
    t=threading.Thread(target=mrkl,args=(ws,))
    t.start()

def on_message(ws, message):
    try:
        info=DouyuMsg(message=message).getInfo()
        if info:
            print(info)
    except Exception as err:
        print('*** message parse err ***')
        print(message,err)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    wsdanmumain()

def on_open(ws):
    print('### open ###')
    login(ws,str(conf.room_num),conf.username,conf.uid)
    join(ws,str(conf.room_num))
    keepalive(ws)



def wsdanmumain():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://danmuproxy.douyu.com:8503/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    wsdanmumain()
