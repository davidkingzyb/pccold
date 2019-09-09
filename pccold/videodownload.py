import re
import os
import logging
from .config import conf
import requests

room_obj_list=[]

from .tools import read,saveStream,ReturnCodeObserverThread,SleepKillerThread
from .bypyrm import doBypy

isinit=False

#log set
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%m/%d %H:%M:%S',
                filename=conf.log_path,
                filemode='a')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

def getRoomObjList():
    global room_obj_list
    global isinit
    global conf
    files=os.listdir(conf.download_path)
    if isinit:
        return room_obj_list
    logging.info('init room obj list')
    md=read(conf.videolist_path)
    lines=md.split('\n')
    for l in lines:
        match=re.match(r'\[(.*)\]\((.*)\)',l)
        if l and match:
            room_obj={'file_name':match.group(1)+'.mp4','url':match.group(2)}
            if room_obj.get('file_name','') in files:
                logging.info(room_obj.get('file_name','')+' is exist')
            else:
                room_obj_list.append(room_obj)
    isinit=True
    return room_obj_list
    

def downloadVideo():
    global conf
    print('videodownload main')
    room_obj_list=getRoomObjList()
    if len(room_obj_list)>0:
        room_obj=room_obj_list.pop()
        saveStream('source',room_obj.get('file_name','default.mp4'),url=room_obj.get('url',''))
    elif conf.is_bypy:
        doBypy()

def reqVideoList(author):
    global room_obj_list
    global isinit
    if isinit:
        return room_obj_list
    result=[]
    api='https://v.douyu.com/show/'
    url="https://v.douyu.com/video/author/getAuthorShowAndVideoList?up_id={author}".format(author=author)
    data=requests.get(url).json()
    ls=data.get('data').get('list')
    for l in ls:
        vls=l.get('video_list')
        for ll in vls:
            title=ll.get('title')
            print(title)
            file_name=re.sub(r"[\/\\\:\*\?\"\<\>\| \$\^\+\-\!]",'_',title)
            result.append({'url':api+ll.get('hash_id'),'file_name':file_name+'.mp4'})
    room_obj_list=result
    isinit=True
    return result

def download3DaysVideo():
    global conf
    room_obj_list=reqVideoList(conf.video_author)
    if len(room_obj_list)>0:
        room_obj=room_obj_list.pop()
        saveStream('source',room_obj.get('file_name','default.mp4'),url=room_obj.get('url',''))
    elif conf.is_bypy:
        doBypy()

if __name__ == '__main__':
    downloadVideo()
