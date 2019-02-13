# coding: utf-8
"""
===================================================
                                                   
                                     __            
 _______  ______   ______    _____  |  |       ___ 
|   __  ||   ___| |   ___|  /     \ |  |   ___|   |
|    ___||  |____ |  |____ |   o   ||  |_ |  ___  |
|___|    |_______||_______| \_____/ |____||_______|
===================================================
2017/8/5 by DKZ https://davidkingzyb.github.io

"""

#http://www.douyu.com/lapi/live/getPlay/20360

import requests
import tools
import conf

getPlay_req='did=BD02A01C3269148CB4C489DFB81B0188&sign=6e043656516e320e3731e6918a400ace&ver=2017080521&rate=2&tt=25035410&cptl=0002&cdn='

def getRtmpUrl(req):
    data=requests.post('http://www.douyu.com/lapi/live/getPlay/20360',req)
    resp=data.json()
    rtmp_url=resp['data']['rtmp_url']+'/'+resp['data']['rtmp_live']
    return rtmp_url

def main():
    try: input = raw_input
    except NameError: pass
    print('Block request http://www.douyu.com/lapi/live/getPlay/(roomid)')
    print('Enter getPlay request query:')
    req=input()
    if req:
        rtmp_url=getRtmpUrl(req)
        print('### rtmp_url: ',rtmp_url)
        tmpl=tools.read(conf.manual_tmpl_path).replace('<rtmp_url>',rtmp_url)
    else:
        tmpl=tools.read(conf.now_tmpl_path)
    tools.write(conf.douyutv_plug_path,tmpl)
    print('\n\n copy douyutv.py plug ok')
    print('streamlink http://www.douyutv.com/cold medium -o ')



if __name__ == '__main__':
    main()