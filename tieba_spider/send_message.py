# -*- coding: utf-8 -*-
import time
import sqlite3
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
from email.utils import formataddr,parseaddr

#格式化邮件地址
def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr(( \
    Header(name, 'utf-8').encode(), \
    addr.encode('utf-8') if isinstance(addr, unicode) else addr))

#设置邮件发送者的email
sender = 'XXXXXXXXX@163.com' 
#设置邮件接收者的email
receiver = 'XXXXXXXXX@qq.com'  
#设置主题
subject = 'XXXXXXXXX'  
#SMTP服务器地址
smtpserver = 'smtp.163.com'
#你需要登录邮件发送者的账号
username = 'XXXXXXXXX@163.com'  
#你需要登录邮件发送者的密码
password = 'XXXXXXXX' 
#与数据库交互
conn=sqlite3.connect("E:/test1.db")
sql = "CREATE TABLE IF NOT EXISTS Tieba(id integer PRIMARY KEY autoincrement,title varchar(100),time varchar(50),url varchar(100) UNIQUE)"

conn.execute(sql)
cs = conn.cursor()

#每次从数据库取数据从0开始
id2 = 0  
while 1==1:
	note = ''
	print u'<<<<<<<<<<<<<<<<<<<<<<<<go on>>>>>>>>>>>>>>>>>>>>>>>：'
	cs.execute("select max(id) from Tieba")
	for j in cs:
		#将数据库最新的一条数据的id赋给id1
		id1 = j[0]
	try:
		if id1>id2:
			#每次只取出数据库新增的数据
			cs.execute("select * from Tieba where id>%s"%id2)
			for i in cs:
				#将一整条数据赋值给note1
				note1 = i
				#将数据拆分，并重新组装
				note=note+note1[1]+" -- "+note1[2]+" -- "+note1[3]+'\n'

				print u"""
--------------------------------------------------------------------------------"""
			#将消息的格式进行准换
			msg = MIMEText(note,_subtype='plain',_charset='utf-8')

			msg['Subject'] = Header(subject, 'utf-8') 
			msg['From'] = _format_addr(u'欢迎订阅我的贴吧动态 <%s>' % sender)
			msg['To'] = _format_addr(u'管理员 <%s>' % receiver)
			conn.commit()

			#登录邮箱
			smtp = smtplib.SMTP()  
			smtp.connect('smtp.163.com')  
			smtp.login(username, password) 
			#发送邮件 
			smtp.sendmail(sender, receiver, msg.as_string())

			#将数据库中最新一条数据的id赋给id2
			id2=id1
			time.sleep(60)
		else:
			time.sleep(60)
	except Exception:
			pass
cs.close()
conn.close()
smtp.quit()