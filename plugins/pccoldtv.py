import subprocess
import hashlib
import re
import time
import uuid

from requests.adapters import HTTPAdapter
from streamlink.plugin import Plugin
from streamlink.plugin.api import http, validate, useragents
from streamlink.stream import HTTPStream, HLSStream, RTMPStream

import requests
import execjs
from pccold.config import conf

# https://github.com/wbt5/real-url/blob/master/douyu.py

def get_tt():
    tt1 = str(int(time.time()))
    tt2 = str(int((time.time() * 1000)))
    today = time.strftime('%Y%m%d', time.localtime())
    return tt1, tt2, today


def get_homejs(rid):
    room_url = 'https://m.douyu.com/' + rid
    response = requests.get(url=room_url)
    pattern_real_rid = r'"rid":(\d{1,7})'
    real_rid = re.findall(pattern_real_rid, response.text, re.I)[0]
    if real_rid != rid:
        room_url = 'https://m.douyu.com/' + real_rid
        response = requests.get(url=room_url)
    homejs = ''
    pattern = r'(function ub9.*)[\s\S](var.*)'
    result = re.findall(pattern, response.text, re.I)
    str1 = re.sub(r'eval.*;}', 'strc;}', result[0][0])
    homejs = str1 + result[0][1]
    return homejs, real_rid


def get_sign(rid, post_v, tt, ub9):
    docjs = execjs.compile(ub9)
    res2 = docjs.call('ub98484234')
    str3 = re.sub(r'\(function[\s\S]*toString\(\)', '\'', res2)
    md5rb = hashlib.md5((rid + '10000000000000000000000000001501' + tt + '2501' +
                         post_v).encode('utf-8')).hexdigest()
    str4 = 'function get_sign(){var rb=\'' + md5rb + str3
    str5 = re.sub(r'return rt;}[\s\S]*','return re;};', str4) 
    str6 = re.sub(r'"v=.*&sign="\+', '', str5)
    docjs1 = execjs.compile(str6)
    sign = docjs1.call(
        'get_sign', rid, '10000000000000000000000000001501', tt)
    return sign


def mix_room(rid):
    result1 = 'PKing'
    return result1


def get_pre_url(rid, tt):
    request_url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + rid
    post_data = {
        'rid': rid,
        'did': '10000000000000000000000000001501'
    }
    auth = hashlib.md5((rid + str(tt)).encode('utf-8')).hexdigest()
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'rid': rid,
        'time': tt,
        'auth': auth
    }
    response = requests.post(url=request_url, headers=header, data=post_data)
    response = response.json()
    pre_url = ''
    if response.get('error') == 0:
        real_url = (response.get('data')).get('rtmp_live')
        if 'mix=1' in real_url:
            pre_url = mix_room(rid)
        else:
            pattern1 = r'^[0-9a-zA-Z]*'
            pre_url = re.search(pattern1, real_url, re.I).group()
    return pre_url


def get_sign_url(post_v, rid, tt, ub9):
    sign = get_sign(rid, post_v, tt, ub9)
    request_url = 'https://m.douyu.com/api/room/ratestream'
    post_data = {
        'v': '2501' + post_v,
        'did': '10000000000000000000000000001501',
        'tt': tt,
        'sign': sign,
        'ver': '219032101',
        'rid': rid,
        'rate': '1'
    }
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
    }
    response = requests.post(url=request_url, headers=header, data=post_data).json()
    print('resp',response)
    if response.get('code') == 0:
        real_url = (response.get('data')).get('url')
        if 'mix=1' in real_url:
            result1 = mix_room(rid)
        else:
            pattern1 = r'live/(\d{1,8}[0-9a-zA-Z]+)_?[\d]{0,4}/playlist'
            result1 = re.findall(pattern1, real_url, re.I)[0]
    else:
        result1 = 0
    return result1


def get_real_url(rid):
    rid = str(rid)
    tt = get_tt()
    url = get_pre_url(rid, tt[1])
    if url:
        return "http://tx2play1.douyucdn.cn/live/" + url +"_"+conf.stream_type +".flv?uuid="
    else:
        result = get_homejs(rid)
        real_rid = result[1]
        homejs = result[0]
        real_url = get_sign_url(tt[2], real_rid, tt[0], homejs)
        if real_url != 0:
            real_url = "http://tx2play1.douyucdn.cn/live/" + real_url + "_"+conf.stream_type +".flv?uuid="
        else:
            real_url = '未开播'
        return real_url

def get_url_from_js(rid):
    # 从播放页源代码中直接匹配地址
    header = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.get('https://www.douyu.com/{}'.format(rid), headers=header).text
        real_url = re.findall(r'live/({}[\d\w]*?)_'.format(rid), response)[0]
    except:
        real_url = '直播间未开播或不存在'
    return "http://dyscdnali1.douyucdn.cn/live/" + real_url +"_"+conf.stream_type +".flv?uuid="

# puppteer

def getPlay():
    js=subprocess.Popen(['node','index.js'],stdout=subprocess.PIPE)
    stdout,stderr=js.communicate()
    returncode=js.wait() # 0 ok , 1 not get url , 3 time out , 4 error
    print('return code',returncode)
    print(stdout.decode())
    if returncode==0 and '$$$$' in stdout.decode():
        return stdout.decode().split('$$$$')[1]
    else:
        exit(returncode)


# plugin

# rtmp_url=getPlay()
# rtmp_url=get_real_url(9999) #room id

STREAM_WEIGHTS = {
    'default':1
}

_url_re = re.compile(r"""
    http(s)?://
    (?:
        (?P<subdomain>.+)
        \.
    )?
    douyu.com/
    (?:
        show/(?P<vid>[^/&?]+)|
        (?P<channel>[^/&?]+)
    )
""", re.VERBOSE)


class PcCold(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return url=='https://pccold'
        # return _url_re.match(url)

    @classmethod
    def stream_weight(cls, stream):
        if stream in STREAM_WEIGHTS:
            return STREAM_WEIGHTS[stream], "pccold"
        return Plugin.stream_weight(stream)

    def _get_streams(self):  
        rtmp_url=get_real_url(conf.room_id) #room id
        if 'rtmp:' in rtmp_url:
            stream = RTMPStream(self.session, {
                    "rtmp": rtmp_url,
                    "live": True
                    })
            yield 'default', stream
        else:
            yield 'default', HTTPStream(self.session, rtmp_url)

__plugin__ = PcCold 
