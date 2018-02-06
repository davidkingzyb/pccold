# coding:utf-8
# 2018/2/6 by DKZ


import socket,re,threading,time,logging
import conf

logging.basicConfig(level=logging.INFO,
                format='%(message)s',
                filename='danmu.log',
                filemode='w')

HOST='openbarrage.douyutv.com'
PORT=8601

class Danmu(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.codeLocalToServer = 689
        self.serverToLocal = 690
        self.gid = -9999 #all danmu group id
        self.rid = conf.room_num #room id

    def sendMsg(self,msg):
        msg = msg.encode('utf-8')
        data_length= len(msg)+8
        msg_head=int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(self.codeLocalToServer,4,'little')
        self.sock.send(msg_head)
        self.sock.sendall(msg)

    def login(self):
        msg='type@=loginreq/roomid@='+str(self.rid)+'/\x00'
        self.sock.connect((HOST, PORT))
        self.sendMsg(msg)
        data = self.sock.recv(1024)
        logging.info('### login\t\t'+ repr(data))

    def join(self):
        msg='type@=joingroup/rid@='+str(self.rid)+'/gid@='+str(self.gid)+'/\x00'  
        self.sendMsg(msg)
        data = self.sock.recv(1024)
        logging.info('### join\t\t'+ repr(data))

    def keeplive(self):
        while True:
            msg='ttype@=mrkl/\x00'
            self.sendMsg(msg)
            data = self.sock.recv(1024)
            now_time=time.strftime('_%m_%d_%H_%M',time.localtime(time.time()))
            logging.info('### keeplive'+now_time)
            time.sleep(40)

    def recv(self):
        while True:
            data = self.sock.recv(1024)
            # logging.info(repr(data))
            self.dataProcess(data)

    def dataProcess(self,data):
        d = re.search(b'type@=(\w*)', data)
        if d:
            if d.group(1)==b'chatmsg':
                danmu = re.search(b'nn@=(.*)/txt@=(.*?)/',data)
                try:
                    logging.info(danmu.group(1).decode()+':::'+danmu.group(2).decode())
                except BaseException as e:
                    logging.info("### *** chatmsg Error",danmu)
            elif d.group(1)==b'uenter':
                user = re.search(b'uid@=(.*)/nn@=(.*?)/',data)
                try:
                    logging.info(user.group(2).decode()+'@@@'+user.group(1).decode())
                except BaseException as e:
                    logging.info("### *** uenter Error",user)
            elif d.group(1)==b'al':
                logging.info('### cold leave')
            elif d.group(1)==b'ab':
                logging.info('### cold back')
            elif d.group(1)==b'upbc':
                logging.info('### cold level up')


if __name__ == '__main__':
    danmu = Danmu()
    danmu.login()
    danmu.join()
    threading.Thread(target=danmu.keeplive).start()
    danmu.recv()

