# coding: utf-8
import smtplib
from email.mime.text import MIMEText
import dkzsecret
import optparse

host=dkzsecret.mailhost
port=25
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

    print 'send email to %s <%s> ok'%(to,subj)

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