#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,urllib,httplib,smtplib
from email.MIMEText import MIMEText 
from email.Header import Header
import datetime
import MySQLdb
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
user_num=1
phone_num=1
new_user=1
new_phone=1


reload(sys)
sys.setdefaultencoding('utf-8')

mail_user = 'noreply@halove.com'
mail_passwd = 'xxxxxxxxxxxxzyKL'
mail_server='123.58.xxx.xx'
mail_port = '465'
mail_to=['daohe@halove.com', 'alan@halove.com', 'zhousq@halove.com']
mail_subjet='bi数据统计'
mail_body=''


def query():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    user_num_sql="SELECT count(*) FROM user_member where create_time<='" +str(today)+" 20:00:00';"
    phone_num_sql="SELECT count(*) FROM user_member WHERE USE_9I_PHONE=1 AND TYPE=0 AND create_time<='" +str(today)+" 20:00:00';"
    new_user_num_sql="SELECT count(*) FROM user_member WHERE create_time<='"+str(today)+" 20:00:00' AND create_time>='"+str(yesterday)+" 20:00:00';"
    new_phone_num_sql="SELECT count(*) FROM user_member WHERE USE_9I_PHONE=1 AND TYPE=0 AND create_time<='"+str(today)+" 20:00:00' AND create_time>='"+str(yesterday)+" 20:00:00';"
    #print user_num_sql
    #print phone_num_sql
    #print new_user_num_sql
    #print new_phone_num_sql
    conn=MySQLdb.connect(host="xxxxxxxxxxx.mysql.rds.aliyuncs.com",user='xxxxxx',passwd='xxxxxxxxxx',db='xxxxxx',charset="utf8")

    cur = conn.cursor()

    cur.execute(user_num_sql)
    user_num_data = cur.fetchone()

    cur.execute(phone_num_sql)
    phone_num_data = cur.fetchone()

    cur.execute(new_user_num_sql)
    new_user_num_data = cur.fetchone()

    cur.execute(new_phone_num_sql)
    new_phone_num_data = cur.fetchone()

    conn.close()
    user_num=user_num_data[0]
    #print user_num
    phone_num=phone_num_data[0]
    new_user=new_user_num_data[0]
    new_phone=new_phone_num_data[0]


    mail_body='统计区间：'+str(yesterday)+'晚20:00－'+str(today)+"晚20:00 \n \
总数: \n \
九爱用户："+str(user_num)+'　　九爱手机用户：'+str(phone_num)+" \n \
新增: \n \
用户数："+str(new_user)+'　九爱手机用户：'+str(new_phone)
    smtp = smtplib.SMTP_SSL(mail_server,mail_port)
    #smtp.set_debuglevel(1)
    smtp.login(mail_user, mail_passwd)
    
    subject = mail_subjet
    body = mail_body

    encoding = 'utf-8'
    
    msg = MIMEText(body.encode(encoding),'plain',encoding)
    msg['Subject'] = Header(subject,encoding)
    msg['From'] = Header('周盛强', 'utf-8')
    msg['To'] = Header('alen,稻荷', 'utf-8')
    
    smtp.sendmail(mail_user,mail_to,msg.as_string() )
    smtp.quit()



if __name__ == '__main__':
    query()


