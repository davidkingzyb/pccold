"""

license:MIT

Copyright (c) 2016 DKZ

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

==============================================================================================================================
 __    __                   ________                          ________                                                        
|  |  |  |                 |__    __|                   __   |   _____|                           _      __                   
|  |/\|  |  _____  ___        |  |     _____    _____  |  |  |  |____   __  __  ______   ______  | \_   |__|  _____   ______  
|        | /  _  \|   |___    |  |    /     \  /     \ |  |  |   ____| |  | | ||      \ |   ___| |   _| |  | /     \ |      \ 
|   /\   |/  ____/|  ___  |   |  |   |   o   ||   o   ||  |_ |  |      |  |_| ||   _   ||  |____ |  |___|  ||   o   ||   _   |
|__/  \__|\______/|_______|   |__|    \_____/  \_____/ |____||__|      |______||__| |__||_______|\_____/|__| \_____/ |__| |__|
==============================================================================================================================
2016/05/23 by DKZ https://davidkingzyb.github.io
github: https://github.com/davidkingzyb/WebToolFunction


"""
from HTMLParser import HTMLParser
import urllib2
import urllib
import re

def removeTags(html):
    return re.sub('<.+?>','',html)

def removeEntityref(html):
    return re.sub('&.+?;','',html)


def subString(string,start,end):
    s=string.find(start)+len(start)
    e=string.find(end,s)
    return string[s:e]

def subAllString(string,start,end):
    r=[]
    s=string.find(start)+len(start)
    e=string.find(end,s)
    r.append(string[s:e])
    s=string.find(start,e)
    while s>0:
        e=string.find(end,s)
        r.append(string[s+len(start):e])
        s=string.find(start,e)
    return r 

def spider(url,cookie='',ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'):
    req=urllib2.Request(url)
    req.add_header('Cookie',cookie)
    req.add_header('User-Agent',ua)
    resp=urllib2.urlopen(req)
    html=resp.read()
    return html

def post(url,data):
    resp=urllib2.urlopen(url=url,data=urllib.urlencode(data))
    r=resp.read()
    return r

class getAttr(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.arr=[]
        self.targetAttr=''
        self.selectAttrName=''
        self.selectTagName=''
        self.selectAttrValue=''

    def getResult(self):
        return self.arr

    def setTargetAttr(self,targetattr):
        self.targetAttr=targetattr


    def setTagSelector(self,tagname):
        self.selectTagName=tagname

    def setAttrSelector(self,attrname,attrvalue):
        self.selectAttrName=attrname
        self.selectAttrValue=attrvalue

    def handle_starttag(self, tag, attrs):
        if self.selectTagName!='' and self.selectAttrName!='':
            isAttr=False
            for x in attrs:
                if x[0]==self.selectAttrName and x[1]==self.selectAttrValue:
                    isAttr=True
            if tag==self.selectTagName and isAttr:
                for x in attrs:
                    if x[0]==self.targetAttr:
                        self.arr.append(x[1])
        else:
            if self.selectAttrName!='':
                for x in attrs:
                    if x[0]==self.selectAttrName and x[1]==self.selectAttrValue:
                        for x in attrs:
                            if x[0]==self.targetAttr:
                                self.arr.append(x[1])
            else:
                if tag==self.selectTagName:
                    for x in attrs:
                        if x[0]==self.targetAttr:
                            self.arr.append(x[1])

    def handle_startendtag(self, tag, attrs):
        if self.selectTagName!='' and self.selectAttrName!='':
            isAttr=False
            for x in attrs:
                if x[0]==self.selectAttrName and x[1]==self.selectAttrValue:
                    isAttr=True
            if tag==self.selectTagName and isAttr:
                for x in attrs:
                    if x[0]==self.targetAttr:
                        self.arr.append(x[1])
        else:
            if self.selectAttrName!='':
                for x in attrs:
                    if x[0]==self.selectAttrName and x[1]==self.selectAttrValue:
                        for x in attrs:
                            if x[0]==self.targetAttr:
                                self.arr.append(x[1])
            else:
                if tag==self.selectTagName:
                    for x in attrs:
                        if x[0]==self.targetAttr:
                            self.arr.append(x[1])

def testgetAttr():
    html='<a id="dkz" href="hello"></a>'
    parser=getAttr()
    parser.setTargetAttr('href')
    parser.setTagSelector('a')
    parser.setAttrSelector('id','dkz')
    parser.feed(html)
    arr=parser.getResult()
    print(arr)

def testspider():
    print(spider('http://davidkingzyb.github.io'))

def testsubString():
    string='<aaa>xxxxfx<bbb><aaa>fieaje<bbb>'
    print(subString(string,'<aaa>','<bbb>'))
    print(subAllString(string,'<aaa>','<bbb>'))

def testpost():
    r=post('http://127.0.0.1:5000/io',{'tty':'help'})
    print(r)

if __name__ == '__main__':
    testgetAttr()
    # testspider()
    #testsubString()
    # testpost()


