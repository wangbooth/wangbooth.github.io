#coding: utf-8

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import traceback

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(smtp_server_ip, smtp_server_port, smtp_username, smtp_password, \
                from_addr={}, to_addrs=[], cc_addrs=[], bcc_addrs=[], \
                title='', text='', html='', images={}, files={}):
    
    # smtp login 
    try:
        s = smtplib.SMTP(smtp_server_ip, smtp_server_port)
        s.login(smtp_username, smtp_password)
    except Exception as err:
        print("smtp login error: " + str(err))
        traceback.print_tb(err.__traceback__)
        return -1

    # msg
    msg = MIMEMultipart()
    msg['From'] = _format_addr(from_addr['nickname'] + ' <' + from_addr['addr'] + '>')
    msg['To'] = ','.join(to_addrs)
    msg['Cc'] = ','.join(cc_addrs)
    msg['Bcc'] = ','.join(bcc_addrs)

    # title
    msg['Subject'] = Header(title, "utf-8")

    # text
    text_msg = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_msg)

    # html
    html_msg = MIMEText(html, 'html', 'utf-8')
    msg.attach(html_msg)

    # image
    if len(images) > 0 :
        for path, name in images.items():
            if os.path.exists(path):
                image = MIMEImage(open(path,'rb').read())
                image.add_header("Content-Disposition", "attachment", filename=name)
                image.add_header('Content-ID', '<0>')
                image.add_header('X-Attachment-Id', '0')

                msg.attach(image)
            else:
                print("file(%s) not exist" % path )
                return -2
    # file
    if len(files) > 0 :
        for path, name in files.items():
            if os.path.exists(path):
                att = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
                att.add_header("Content-Type", 'application/octet-stream')
                att.add_header("Content-Disposition", "attachment", filename=name)
                msg.attach(att)
            else:
                print("file(%s) not exist" % path )
                return -2
    s.send_message(msg)
    return 0

if __name__  == "__main__":
    smtp_server_ip = 'smtp.126.com'
    smtp_server_port = 25
    smtp_username = 'wangbooth@126.com'
    smtp_password = 'wang0000'
    from_addr={'nickname': '网布斯', 'addr': 'wangbooth@126.com' }
    to_addrs=['wang_baomi@163.com', 'wangbooth@gmail.com']
    cc_addrs=['system1029@gmail.com']
    bcc_addrs=['baomi.wbm@dtwave-inc.com']
    title='报告内容'
    text='以下是测试报告内容:\n换行后'
    html='<b>这个是加粗的</b>'
    images={'test.png': '测试图片.png', 'send_ok1.png': '第二章图片.png'}
    files={'solution.pdf': '测试pdf文件.pdf', 'test.txt': '测试txt文件.txt'}

    send_mail(smtp_server_ip, smtp_server_port, smtp_username, smtp_password, \
                    from_addr, to_addrs, cc_addrs, bcc_addrs, \
                    title, text, html, images, files)

