# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import dkzsecret
import optparse

host=dkzsecret.mailhost
port=25 #exmail.qq 465 or 25
sender=dkzsecret.mailsender
pwd=dkzsecret.mailpwd

def sendEmail(subj,to,body):
    msg=MIMEText(body,'plain','utf-8')
    msg['subject']=subj
    msg['from']=sender
    msg['to']=to

    server=smtplib.SMTP(host,port)
    # server.set_debuglevel(1)
    server.login(sender,pwd)
    server.sendmail(sender,to,msg.as_string())
    server.quit()
    # print('send email to %s <%s> ok'%(to,subj))

pccoldfooter="\n\n这是一条冷布丁的自动开播提醒～\n请继续支持 @冷了个冷\n\n如需订阅或退订请联系我\n此外，这个项目有自动录冷冷的视频功能，不定期上传云盘\n\n"
pccoldcontact="\npccold by DKZ \n---------------------\ngithub:https://github.com/davidkingzyb/pccold\ncontact:davidkingzyb@163.com  @__DKZ__\naboutme:http://davidkingzyb.github.io\n"

def pccold(roomobj,to):
    subj='[pccold]'+roomobj['data']['room_name']+'@'+roomobj['data']['owner_name']
    body='\nroom_name:'+roomobj['data']['room_name']
    body+='\nowner_name:'+roomobj['data']['owner_name']+'#'+roomobj['data']['room_id']
    body+='\nstart_time:'+roomobj['data']['start_time']
    body+='\ncate_name:'+roomobj['data']['cate_name']
    body+='\nlink:http://www.douyutv.com/'+roomobj['data']['room_id']
    #body+=pccoldfooter
    body+=pccoldcontact
    sendEmail(subj,to,body)


def main():
    parser=optparse.OptionParser('-s <subj> -t <to> -m <msg>')
    parser.add_option('-s',dest='subj',type='string')
    parser.add_option('-t',dest='to',type='string')
    parser.add_option('-m',dest='msg',type='string')
    (option,args)=parser.parse_args()
    if(option.subj==None or option.to==None or option.msg==None):
        print parser.usage
        exit(0)
    else:
        sendEmail(option.subj,option.to,option.msg)
        print 'ok'


if __name__ == '__main__':
    main()
