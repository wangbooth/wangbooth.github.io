#coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

textfile = "test.txt"
me = "wangbooth@126.com"
you = "wangbooth@gmail.com"

new_msg = MIMEMultipart()
msg = None
# open()中增加一个参数encoding='utf-8'
with open(textfile, encoding='utf-8') as fp:
    msg = MIMEText(fp.read())
    # new_msg.attach(text_msg)

msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

# msg['Cc'] = "wang_baomi@163.com"
# msg['Bcc'] = "system1029@gmail.com"


new_msg['Subject'] = 'The contents of %s' % textfile
new_msg['From'] = me
new_msg['To'] = you

# new_msg['Cc'] = "wang_baomi@163.com"
# new_msg['Bcc'] = "system1029@gmail.com"



s = smtplib.SMTP('smtp.126.com', 25)
s.login(me, "wang0000")

s.send_message(msg)
# s.send_message(new_msg)
s.quit()